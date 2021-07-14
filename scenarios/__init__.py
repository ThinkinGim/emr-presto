from pickle import NONE
from aws_cdk import core
from artifacts import (
    infra,
    emr,
)

class EmrPrestoStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # network = infra.Network(self, 'Network')
        emr.Cluster(self, 'Presto', bmt_vpc=None)
