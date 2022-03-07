"""
CDK Pipelines Stack.
"""
from aws_cdk import (
    Stack,
    pipelines as pipelines,
    aws_ssm as ssm,
    aws_iam as iam,
)
from constructs import Construct
from pipeline_stages.static_website_deploy_stage import StaticWebsiteDeployStage


class PipelineStack(Stack):
    """
    Creates a CDK Pipeline to deploy resources using CDK.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        static_website_deploy_stage: StaticWebsiteDeployStage,
        **kwargs
    ):
        """
        Creates a CDK Pipeline to deploy resources using CDK.
        :param scope: Scope in which stack is created.
        :param construct_id: ID of stack construct.
        :param static_website_deploy_stage: Stage which deploys stack for static website deployment.
        :param kwargs: Extra keyword arguments.
        """
        super().__init__(scope, construct_id, **kwargs)
        source = pipelines.CodePipelineSource.connection(
            "KMK-Git/kaustubhk-blogs",
            "main",
            connection_arn=ssm.StringParameter.value_for_string_parameter(
                self,
                "codestar_connection_arn",
            ),
        )
        cdk_codepipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.CodeBuildStep(
                "Synth",
                input=source,
                install_commands=[
                    "cd site-code",
                    "npm ci",
                    "cd ../cdk-code",
                    "pip install -r requirements.txt -r requirements-dev.txt",
                    "npm install -g aws-cdk",
                ],
                commands=[
                    "cd ../site-code",
                    "npm run lint",
                    "npm run test",
                    "npm run build",
                    "cd ../cdk-code",
                    "black .",
                    "pylint application_stacks pipeline_stages pipeline_stack tests app.py",
                    "pytest --cov=.",
                    "cdk synth",
                ],
                primary_output_directory="cdk-code/cdk.out",
                role_policy_statements=[
                    iam.PolicyStatement(
                        actions=["sts:AssumeRole"],
                        resources=["*"],
                        conditions={
                            "StringEquals": {
                                "iam:ResourceTag/aws-cdk:bootstrap-role": "lookup",
                            },
                        },
                    ),
                ],
            ),
        )
        cdk_codepipeline.add_stage(
            static_website_deploy_stage,
            pre=[
                pipelines.ConfirmPermissionsBroadening(
                    "CheckPermissions", stage=static_website_deploy_stage
                ),
            ],
        )
