"""
Static Website CDK Stage.
"""
import aws_cdk as cdk
from constructs import Construct
from application_stacks.static_website_stack import StaticWebsiteStack


class StaticWebsiteDeployStage(cdk.Stage):
    """
    Create infrastructure required for a static application in AWS.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        hostedzone_domain_name: str,
        website_subdomain: str,
        **kwargs
    ):
        """
        Create infrastructure required for a static application in AWS.
        :param scope: Scope in which stage is created.
        :param construct_id: ID of stack construct.
        :param hostedzone_domain_name: Domain name of Route 53 hosted zone.
        :param website_subdomain: Subdomain for static website.
        :param kwargs: Extra keyword arguments.
        """
        super().__init__(scope, construct_id, **kwargs)
        self.stack = StaticWebsiteStack(
            self,
            "StaticWebsiteStack",
            hostedzone_domain_name=hostedzone_domain_name,
            website_subdomain=website_subdomain,
        )
