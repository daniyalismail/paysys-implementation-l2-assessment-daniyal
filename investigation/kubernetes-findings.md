# Kubernetes Manifest Findings

The starter manifest `broken-api.yaml` contained several defects that would prevent the application from successfully deploying and receiving traffic:

1. **Service Selector Mismatch**: 
   The `Service` has `selector: app: minipay-backend`, but the `Deployment` pods are labeled with `app: minipay-api`. The Service will not route traffic to the pods.
2. **Target Port Mismatch**: 
   The `Service` routes to `targetPort: 8081`, but the container only exposes `containerPort: 8080`.
3. **Readiness Probe Port Mismatch**: 
   The `readinessProbe` attempts to check port `8081`, which does not match the container's exposed port of `8080`.
4. **Missing Container Image**: 
   The `image` field is a placeholder (`YOUR_IMAGE_HERE`), which will result in an `ErrImagePull` or `ImagePullBackOff`.
5. **Missing Resource Limits/Requests**: 
   The manifest lacks CPU and Memory limits and requests, which is considered a bad practice in production environments as it can lead to resource starvation.
6. **Hardcoded Environment Variables**: 
   `DB_HOST` is hardcoded. It is best practice to use `ConfigMap` for configuration (like hosts/ports) and `Secret` for sensitive data (like passwords).

The fixed manifests are provided in the `kubernetes/` directory.
