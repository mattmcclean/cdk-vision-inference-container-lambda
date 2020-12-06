import * as cdk from '@aws-cdk/core';
import * as apigateway from "@aws-cdk/aws-apigateway";
import * as lambda from "@aws-cdk/aws-lambda";
import * as path from 'path';

export class VisionInferenceService extends cdk.Construct {
  constructor(scope: cdk.Construct, id: string) {
    super(scope, id);

    const handler = new lambda.DockerImageFunction(this, 'VisionFunction', {
      code: lambda.DockerImageCode.fromImageAsset(path.join(__dirname, '../docker-handler')),
      memorySize: 1048,
      timeout: cdk.Duration.seconds(30),
    });

    const api = new apigateway.RestApi(this, "vision-api", {
      restApiName: "Vision Service",
      description: "This service implements a vision inference service for Pets."
    });

    const postImageIntegration = new apigateway.LambdaIntegration(handler, {
      requestTemplates: { "application/json": '{ "statusCode": "200" }' }
    });

    api.root.addMethod("POST", postImageIntegration); // POST /
  }
}
