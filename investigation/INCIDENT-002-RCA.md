# INCIDENT-002 Root Cause Analysis

## Incident Summary
**Issue:** Application Unavailable After Deployment
**Priority:** P1

## Observations and Reproduction Steps
1. A new Kubernetes deployment manifest (`broken-api.yaml`) was applied to the cluster.
2. `kubectl get pods` showed that the pods were either not starting (`ImagePullBackOff`) or running but not receiving traffic.
3. Attempting to hit the Service endpoint returned a connection refused or timeout.

## Evidence Gathered
1. `kubectl describe pod <api-pod>` showed `Failed to pull image "YOUR_IMAGE_HERE": rpc error`.
2. After mocking an image to get the pods running, `kubectl get endpoints minipay-api` showed `<none>`.
3. The Service `selector` was `app: minipay-backend`, while the Deployment `template.metadata.labels` was `app: minipay-api`.
4. The Service `targetPort` was `8081`, while the container's exposed port was `8080`.

## Root Cause
Multiple configuration defects in the newly applied manifest:
1. **Invalid Image:** The deployment lacked a valid container image.
2. **Selector Mismatch:** The Service could not find the Pods because the labels did not match, resulting in empty endpoints.
3. **Port Mismatch:** Even if endpoints matched, the Service was routing traffic to the wrong target port (8081 instead of 8080).

## Immediate Corrective Action
1. Fixed the `image` field to point to a valid container registry image.
2. Corrected the Service `selector` to `app: minipay-api`.
3. Updated the Service `targetPort` to `8080` (and fixed the `readinessProbe` port to `8080`).
4. Re-applied the manifest using `kubectl apply -f minipay.yaml`.

## Permanent Corrective/Preventive Action
- **CI/CD Validation:** Implement `kubeval` or `polaris` in the CI/CD pipeline to automatically catch missing images, invalid selectors, and port mismatches before deployment.
- **Helm Charts / Kustomize:** Use a templating engine to ensure that labels and selectors are centrally defined and cannot diverge by accident.

## Validation Performed
Ran `kubectl get endpoints minipay-api` and verified that pod IPs were listed. Accessed the API via the service port and received a valid `200 OK` health check response.
