
data "aws_iam_policy_document" "statemachine-permissions-policy" {
  statement {
    effect = "Allow"

    resources = ["*"]
 
    actions = ["lambda:InvokeFunction"]
  }
  statement {
    effect = "Allow"

    resources = ["*"]
 
    actions = ["states:RedriveExecution", "states:StartExecution", "states:StartExecution",
    "states:DescribeExecution","states:StopExecution","events:PutTargets","events:PutRule",
    "events:DescribeRule","xray:PutTraceSegments","xray:PutTelemetryRecords",
    "xray:GetSamplingRules","xray:GetSamplingTargets"]
  }
  
}

data "aws_iam_policy_document" "statemachine-trust-policy" {
  statement {
    effect = "Allow"

    principals {
       type        = "Service"
       identifiers = ["states.amazonaws.com"]
     }
 
    actions = ["sts:AssumeRole"]
  }
}



resource "aws_iam_role" "statemachine-role" {
  name               = "c10-games-terraform-statemachine-role-pipeline"
  assume_role_policy = data.aws_iam_policy_document.statemachine-trust-policy.json
  inline_policy {
    name = "c10-games-inline-step-function"
    policy = data.aws_iam_policy_document.statemachine-permissions-policy.json
  }
}


resource "aws_sfn_state_machine" "c10-games-statemachine-terraform" {
  name     = "c10-games-statemachine-terraform"
  role_arn = aws_iam_role.statemachine-role.arn

  definition = <<EOF
{
  "Comment": "A description of my state machine",
  "StartAt": "Parallel",
  "States": {
    "Parallel": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "Epic Lambda",
          "States": {
            "Epic Lambda": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "OutputPath": "$.Payload",
              "Parameters": {
                "Payload.$": "$",
                "FunctionName": "arn:aws:lambda:eu-west-2:129033205317:function:c10-games-terraform-pipeline-epic:$LATEST"
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2
                }
              ],
              "End": true
            }
          }
        },
        {
          "StartAt": "Steam Lambda",
          "States": {
            "Steam Lambda": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "OutputPath": "$.Payload",
              "Parameters": {
                "Payload.$": "$",
                "FunctionName": "arn:aws:lambda:eu-west-2:129033205317:function:c10-games-terraform-pipeline-steam:$LATEST"
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2
                }
              ],
              "End": true
            }
          }
        },
        {
          "StartAt": "GOG Lambda",
          "States": {
            "GOG Lambda": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "OutputPath": "$.Payload",
              "Parameters": {
                "Payload.$": "$",
                "FunctionName": "arn:aws:lambda:eu-west-2:129033205317:function:c10-games-terraform-pipeline-gog:$LATEST"
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2
                }
              ],
              "End": true
            }
          }
        }
      ],
      "Next": "Pass"
    },
    "Pass": {
      "Type": "Pass",
      "Next": "Parallel (1)"
    },
    "Parallel (1)": {
      "Type": "Parallel",
      "Next": "Success",
      "Branches": [
        {
          "StartAt": "DB Load",
          "States": {
            "DB Load": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "OutputPath": "$.Payload",
              "Parameters": {
                "Payload.$": "$",
                "FunctionName": "arn:aws:lambda:eu-west-2:129033205317:function:c10-games-terraform-load:$LATEST"
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2
                }
              ],
              "End": true
            }
          }
        },
        {
          "StartAt": "Alert Lambda",
          "States": {
            "Alert Lambda": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "OutputPath": "$.Payload",
              "Parameters": {
                "Payload.$": "$",
                "FunctionName": "arn:aws:lambda:eu-west-2:129033205317:function:c10-games-terraform-alert:$LATEST"
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2
                }
              ],
              "End": true
            }
          }
        }
      ]
    },
    "Success": {
      "Type": "Succeed"
    }
  }
}
EOF
}