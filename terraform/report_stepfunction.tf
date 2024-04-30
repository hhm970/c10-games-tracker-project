
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
  name               = "c10-games-terraform-statemachine-role-report"
  assume_role_policy = data.aws_iam_policy_document.statemachine-trust-policy.json
  inline_policy {
    name = "c10-games-inline-step-function-report"
    policy = data.aws_iam_policy_document.statemachine-permissions-policy.json
  }
}


resource "aws_sfn_state_machine" "c10-games-statemachine-terraform-report" {
  name     = "c10-games-statemachine-terraform-report"
  role_arn = aws_iam_role.statemachine-role.arn

  definition = <<EOF
{
  "Comment": "A description of my state machine",
  "StartAt": "Lambda Invoke",
  "States": {
    "Lambda Invoke": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "FunctionName": "arn:aws:lambda:eu-west-2:129033205317:function:c10-games-terraform-weekly-report:$LATEST"
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
EOF
}