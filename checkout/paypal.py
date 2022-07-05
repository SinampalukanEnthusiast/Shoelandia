import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AW7bpDXRG0vUery0Yan8G2qQFDMpJBvywUA1Iav9O-p4hQK4B9WQDQc-xiE9MbbM5ch4-kH-mbgbCNur"
        self.client_secret = "EAdLLTgZquhEK4Pw4JVDt34yr6UjJ8hM9V8gnW4YWjhuWESNtOH1eyT-wommgmw6dey_qBjrGKIsLva7"
        self.environment = SandboxEnvironment(
            client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
