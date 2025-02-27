# bda-workshop



## Getting started

## Prerequisites

* Create Jupyterlab space in Amazon Sagemaker Studio
* Make sure you have the following IAM role permissions
 
### Configure IAM Permissions

The features being explored in the notebook require the following IAM Policies for the execution role being used. If you're running this notebook within SageMaker Studio in your own Account, update the default execution role for the SageMaker user profile to include the following IAM policies. 

```json
        {
            "Sid": "BDAPermissions",
            "Effect": "Allow",
            "Action": [
				"bedrock:CreateDataAutomationProject",
				"bedrock:CreateBlueprint",
				"bedrock:ListDataAutomationProjects",
				"bedrock:UpdateDataAutomationProject",
				"bedrock:GetDataAutomationProject",
				"bedrock:GetDataAutomationStatus",
				"bedrock:InvokeDataAutomationAsync",
				"bedrock:GetBlueprint",
				"bedrock:ListBlueprints",
				"bedrock:UpdateBlueprint",
				"bedrock:DeleteBlueprint",
				"bedrock:CreateDataAutomationProject",
				"bedrock:getBlueprintRecommendation",
				"bedrock:InvokeBlueprintRecommendationAsync"
            ],
            "Resource": "*"
        }
Note - The policy uses wildcard(s) for demo purposes. AWS recommends using least priviledges when defining IAM Policies in your own AWS Accounts


