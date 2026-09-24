# Rancher & Kubernetes Operations

## Cluster and Workload Visibility
In a Rancher environment, after importing or creating the cluster, we navigate to **Cluster Explorer -> Workloads -> Deployments**. Here we can see `minipay-api` and `minipay-ui`.
We can also navigate to **StatefulSets** to view `minipay-db`.
Rancher provides a visual dashboard showing the number of active pods, CPU/Memory utilization, and readiness states.

## Pod Status and Logs
To inspect logs or status:
1. Navigate to the `minipay` namespace in the workload view.
2. Click on the `minipay-api` deployment.
3. Under the "Pods" tab, click the **View Logs** icon (the three horizontal lines) on any pod.
4. This opens a live log stream. If a pod crashes, we can switch to the "Previous" log view to see the exit reason.

## Configuration and Environment Inspection
Rancher allows us to view injected configurations:
1. Go to **Storage -> ConfigMaps** or **Storage -> Secrets**.
2. Clicking `minipay-config` displays the key-value pairs (like `DB_HOST`).
3. Inside a pod's detailed view, the **Environment** tab shows exactly what variables were injected into the container at runtime.

## Scaling, Rollout, and Restarts
- **Scaling:** In the Deployments view, click the "+" or "-" buttons next to the replica count for `minipay-api` to instantly scale it up or down.
- **Rollout/Restart:** Select the `minipay-api` deployment, click the vertical ellipsis (three dots) on the right, and choose **Redeploy**. This triggers a rolling restart of the pods, adhering to the readiness probes to ensure zero downtime.

## Basic Resource and Health Visibility
Rancher's built-in monitoring (often powered by Prometheus/Grafana) provides graphs for CPU, Memory, and Network I/O.
By setting the `resources.requests` and `resources.limits` in our manifests, Rancher can accurately display utilization percentages against the allocated quotas, ensuring the `minipay` namespace doesn't starve other cluster applications.
