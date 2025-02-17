import boto3
from botocore.exceptions import ClientError
import json

def get_document_configuration(document_id, plan_name, plan_document_s3_uri): 
    return {
                "content": {
                    "custom": {
                        "customDocumentIdentifier": {
                            "id": document_id
                        },
                        "s3Location": {
                            "uri": plan_document_s3_uri
                        },
                        "sourceType": "S3_LOCATION"
                    },
                    "dataSourceType": "CUSTOM"
                },
                "metadata": {
                    "inlineAttributes": [
                        {
                            "key": "plan_name",
                            "value": {
                                "stringValue": plan_name,
                                "type": "STRING"
                            }
                        }
                    ],
                    "type": "IN_LINE_ATTRIBUTE"
                }
            }

def create_knowledge_base(bedrock_agent, kb_name, 
                          kb_description, 
                          kb_role_arn,
                          embedding_model_arn,
                          vector_store_collection_arn,
                          vector_store_index_name):
    storage_configuration = {
        'opensearchServerlessConfiguration': {
            'collectionArn': vector_store_collection_arn,
            'fieldMapping': {
                'metadataField': 'text-metadata',
                'textField': 'text',
                'vectorField': 'vector'
            },
            'vectorIndexName': vector_store_index_name
        },
        "type": 'OPENSEARCH_SERVERLESS'
    }
    
    embedding_model_configuration = {
        "bedrockEmbeddingModelConfiguration": {
            "dimensions": 1024
        }
    }
    
    knowledge_base_configuration = {
        'type': 'VECTOR',
        'vectorKnowledgeBaseConfiguration': {
            'embeddingModelArn': embedding_model_arn,
            'embeddingModelConfiguration': embedding_model_configuration
        }
    }    
    try:
        kb_list = bedrock_agent.list_knowledge_bases()
        existing_kb_id = next((kb['knowledgeBaseId'] for 
                               kb in kb_list['knowledgeBaseSummaries']
                               if kb['name'] == kb_name), None)
        if (existing_kb_id):
            print(f'KB already exists with name {kb_name}')
            return existing_kb_id
        else:
            # Create knowledge base
            print(f'Creating new KB with name {kb_name}')
            create_kb_response = bedrock_agent.create_knowledge_base(
                description=kb_description,
                knowledgeBaseConfiguration=knowledge_base_configuration,
                name=kb_name,
                roleArn=role_arn,
                storageConfiguration=storage_configuration
            )
        return create_kb_response['knowledgeBase']['knowledgeBaseId']
    
    except ClientError as e:
        print(f"Error creating knowledge base: {e}")
        raise
        return None

def create_data_source(bedrock_agent, knowledge_base_id, datasource_name='claims-eoc-datasource') :

    data_source_configuration = {
        'type': 'CUSTOM'
    }
    
    chunking_configuration = {
        'chunkingStrategy': 'HIERARCHICAL',
        'hierarchicalChunkingConfiguration': {
            'levelConfigurations': [
                {
                    'maxTokens': 1500
                },
                {
                    'maxTokens': 300
                },
            ],
            'overlapTokens': 60
        }
    }
    
    parsing_configuration = {
        'parsingStrategy': 'BEDROCK_DATA_AUTOMATION'
    }    
    ds_list = bedrock_agent.list_data_sources(knowledgeBaseId=knowledge_base_id)
    existing_ds_id = next((ds['dataSourceId'] for 
                               ds in ds_list['dataSourceSummaries']
                               if ds['name'] == datasource_name), None)
    if (existing_ds_id):
        print(f'Datasource already exists with name {datasource_name}')
        return existing_ds_id
    else:
        create_ds_response = bedrock_agent.create_data_source(
            dataSourceConfiguration=data_source_configuration,
            description='direct injection of claims eoc documents',
            knowledgeBaseId=knowledge_base_id,
            name=datasource_name,
            vectorIngestionConfiguration={
                'chunkingConfiguration': chunking_configuration,
                'parsingConfiguration': parsing_configuration
            }
        )
    return create_ds_response['dataSource']['dataSourceId']
