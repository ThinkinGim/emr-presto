from operator import truediv
from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_emr as emr,
    aws_iam as iam,
)

class Cluster(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, bmt_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # instance_type_config = emr.CfnCluster.InstanceTypeConfigProperty(instance_type="m6g.xlarge")

        instancesConfig = emr.CfnCluster.JobFlowInstancesConfigProperty(
            core_instance_group=emr.CfnCluster.InstanceGroupConfigProperty(
                instance_count=1,
                instance_type="m6g.xlarge"
            ),
            master_instance_group=emr.CfnCluster.InstanceGroupConfigProperty(
                instance_count=1,
                instance_type="m6g.xlarge"
            ),
        )

        bootstrap_action = emr.CfnCluster.BootstrapActionConfigProperty(
            name='ssm', 
            script_bootstrap_action=emr.CfnCluster.ScriptBootstrapActionConfigProperty(path='s3://emr-presto-t/ssm_install.sh') 
        )
        
        emr.CfnCluster(self, "emr-presto",
            name="emr-presto",
            release_label="emr-6.3.0",
            applications=[
                emr.CfnCluster.ApplicationProperty(name="Hadoop"),
                emr.CfnCluster.ApplicationProperty(name="Hive"),
                emr.CfnCluster.ApplicationProperty(name="Pig"),
                emr.CfnCluster.ApplicationProperty(name="Hue"),
                emr.CfnCluster.ApplicationProperty(name="Presto")
            ],
            instances=instancesConfig,
            job_flow_role='TEST-EMR-EC2',
            service_role="EMR_DefaultRole",
            visible_to_all_users=True,
            bootstrap_actions=[bootstrap_action]
        )