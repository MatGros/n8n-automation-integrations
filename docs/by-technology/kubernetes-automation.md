# Kubernetes Automation Guide

## Purpose

This guide covers Kubernetes API integration with n8n, including cluster monitoring, Helm deployment automation, GitOps patterns, and production deployment orchestration.

## Overview

Kubernetes (K8s) automation enables infrastructure-as-code deployment, auto-scaling workflows, cluster health monitoring, and application lifecycle management through n8n integration.

## Kubernetes API Basics

### K8s API Concepts

- **Cluster** — Collection of machines running containerized applications
- **Pod** — Smallest deployable unit (usually one container)
- **Deployment** — Manages ReplicaSets and Pods
- **Service** — Network abstraction for Pod access
- **ConfigMap** — Configuration data storage
- **Secret** — Sensitive data storage
- **Namespace** — Virtual cluster within physical cluster

### API Server Access

```javascript
// n8n HTTP Request - K8s API call
{
  "url": "https://kubernetes.default.svc.cluster.local:443/api/v1/namespaces/default/pods",
  "method": "GET",
  "headers": {
    "Authorization": "Bearer ${{ $credentials.k8s_api_token }}",
    "Content-Type": "application/json"
  }
}
```

## n8n Integration with Kubernetes

### Setting Up Kubernetes Credentials

1. Create service account in K8s cluster
2. Get API token and CA certificate
3. Configure in n8n Settings → Credentials

```bash
# Create service account
kubectl create serviceaccount n8n-automation -n default

# Get API token
kubectl get secret $(kubectl get secret -n default | grep n8n-automation | awk '{print $1}') \
  -o jsonpath='{.data.token}' -n default | base64 --decode

# Get API server URL
kubectl cluster-info | grep 'Kubernetes master'
```

### Kubernetes Credential Configuration

```javascript
{
  "server_url": "https://kubernetes.example.com:6443",
  "api_token": "your-service-account-token",
  "namespace": "default",
  "skip_ssl_verification": false  // Use true for self-signed certs
}
```

## Pod Management Workflows

### Monitor Pod Status

```
[Cron trigger every 5 minutes]
  ↓
[List pods in namespace]
  kubectl get pods -n production
  ↓
[Check pod status]
  ├→ Running: OK
  ├→ Pending: Check events
  ├→ CrashLoopBackOff: Alert + restart
  └→ Failed: Investigate logs
  ↓
[Alert if unhealthy]
  Send Slack notification
```

Implementation:

```javascript
// List pods in namespace
{
  "url": "https://kubernetes.example.com:6443/api/v1/namespaces/production/pods",
  "method": "GET",
  "headers": {
    "Authorization": "Bearer ${{ $credentials.k8s_token }}"
  }
}

// Parse response and check status
const pods = items[0].json.items;
const unhealthyPods = pods.filter(pod =>
  pod.status.phase !== 'Running'
);

if (unhealthyPods.length > 0) {
  // Alert operations team
  await notifySlack({
    channel: '#k8s-alerts',
    text: `Unhealthy pods detected: ${unhealthyPods.length}`,
    pods: unhealthyPods.map(p => ({
      name: p.metadata.name,
      status: p.status.phase,
      reason: p.status.conditions?.[0]?.reason
    }))
  });
}
```

### Auto-Restart Failed Pods

```
[Pod enters CrashLoopBackOff state]
  ↓
[Detect via event listener or polling]
  ↓
[Delete pod to trigger restart]
  DELETE /api/v1/namespaces/{ns}/pods/{name}
  ↓
[K8s controller creates new pod]
  ↓
[Monitor new pod logs]
```

## Helm Deployment Automation

### Helm Basics

Helm packages Kubernetes applications. n8n can automate Helm operations:

### Deploy Helm Chart

```
[New version released]
  ↓
[Pull new Helm chart]
  helm repo add myrepo https://charts.example.com
  helm repo update
  ↓
[Render chart values]
  Configure database, replicas, resources
  ↓
[Validate deployment]
  helm lint myrepo/myapp
  ↓
[Install/Upgrade release]
  helm install myapp myrepo/myapp -f values.yaml
  ↓
[Monitor rollout]
  Check deployment status and pod readiness
```

Using n8n:

```javascript
// Execute Helm upgrade command
{
  "url": "https://kubernetes.example.com:6443/api/v1/namespaces/production/pods",
  "method": "POST",
  "body": {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
      "name": "helm-upgrade-job",
      "namespace": "production"
    },
    "spec": {
      "containers": [{
        "name": "helm",
        "image": "alpine/helm:latest",
        "command": [
          "sh",
          "-c",
          "helm upgrade --install myapp myrepo/myapp -f values.yaml"
        ]
      }],
      "restartPolicy": "Never"
    }
  }
}
```

### Helm Release Monitoring

```
[List Helm releases]
  Get status of all deployments
  ↓
[Check for failed releases]
  Status = deployed vs superseded vs failed
  ↓
[Rollback if needed]
  helm rollback <release> <revision>
  ↓
[Notify team]
  Slack alert on rollback/failure
```

## Cluster Monitoring and Health Checks

### Node Health Monitoring

```javascript
// Check node status
{
  "url": "https://kubernetes.example.com:6443/api/v1/nodes",
  "method": "GET",
  "headers": {
    "Authorization": "Bearer ${{ $credentials.k8s_token }}"
  }
}

// Check for problem conditions
const nodes = items[0].json.items;
const problematicNodes = nodes.filter(node => {
  const conditions = node.status.conditions;
  return conditions.some(c =>
    (c.type === 'NotReady' || c.type === 'MemoryPressure' || c.type === 'DiskPressure') &&
    c.status === 'True'
  );
});

if (problematicNodes.length > 0) {
  await alertOps(`${problematicNodes.length} nodes have issues`);
}
```

### Resource Quota Monitoring

```
[Monitor namespace resource usage]
  ↓
[Check against quotas]
  Current CPU, Memory vs limit
  ↓
[If usage approaching limit]
  ├→ Scale up quota
  ├→ Optimize resource requests
  └→ Alert team
```

## GitOps Integration

### ArgoCD Integration

Continuous deployment from Git:

```
[GitHub: Push new Helm chart version]
  ↓
[ArgoCD detects change]
  ↓
[n8n listens for ArgoCD webhook]
  ↓
[Application syncs to cluster]
  ├→ Old pods terminating
  ├→ New pods starting
  └→ Health checks passing
  ↓
[n8n monitors deployment]
  ├→ Check pod readiness
  ├→ Run smoke tests
  └→ Alert team on completion
```

### Webhook Trigger

```javascript
// n8n webhook endpoint for ArgoCD events
POST /webhook/argocd-sync

{
  "type": "application",
  "action": "sync",
  "application": "myapp",
  "namespace": "production",
  "revision": "abc123",
  "syncStatus": "synced"
}

// Execute post-deployment tests
if (msg.syncStatus === 'synced') {
  // Run smoke tests
  await runHealthChecks(msg.application);
  // Run integration tests
  await runTests(msg.application);
  // Notify deployment
  await notifySlack(`${msg.application} deployed successfully`);
}
```

## Auto-Scaling Workflows

### Horizontal Pod Autoscaling (HPA)

Combine with n8n monitoring:

```
[Monitor metrics (CPU, Memory)]
  ↓
[If usage exceeds threshold]
  ├→ HPA auto-scales pods
  └→ n8n logs the event
  ↓
[Monitor new pods coming online]
  ↓
[If scale-down possible]
  HPA terminates excess pods
```

### Custom Scaling with n8n

```
[Time-based scaling]
  Peak hours: 10 AM - 2 PM
  ↓
[Before peak hours]
  Scale up replicas to 10
  ↓
[After peak hours]
  Scale down to 3 replicas
  ↓
[Cost optimization]
  Reduce cloud spend during off-peak
```

Implementation:

```javascript
// Scale deployment
{
  "url": "https://kubernetes.example.com:6443/apis/apps/v1/namespaces/production/deployments/myapp/scale",
  "method": "PATCH",
  "body": {
    "spec": {
      "replicas": 10  // Scale to 10 replicas
    }
  },
  "headers": {
    "Authorization": "Bearer ${{ $credentials.k8s_token }}",
    "Content-Type": "application/strategic-merge-patch+json"
  }
}
```

## Cluster Backup and Recovery

### Backup Workflows

```
[Cron: Daily backup at 2 AM]
  ↓
[Backup all namespaces]
  kubectl get all -o yaml > backup.yaml
  ↓
[Backup persistent volumes]
  Snapshot database volumes
  ↓
[Upload to S3]
  aws s3 cp backup.yaml s3://backups/
  ↓
[Verify backup integrity]
  Check file size and checksum
  ↓
[Alert team]
  Slack notification of backup completion
```

### Disaster Recovery

```
[Cluster failure detected]
  ↓
[Access backup S3 bucket]
  Download latest backup files
  ↓
[Provision new cluster]
  IaC to create replacement cluster
  ↓
[Restore from backup]
  kubectl apply -f backup.yaml
  ↓
[Verify critical services]
  Health checks on core applications
  ↓
[Switch traffic]
  Update DNS to point to new cluster
```

## Cost Optimization

### Resource Monitoring

```
[Daily analysis]
  ↓
[Identify unused resources]
  Pods with low CPU/memory
  Unused PersistentVolumeClaims
  ↓
[Generate report]
  Cost savings opportunity
  ↓
[Notify team]
  Recommend cleanup
```

### Cleanup Workflow

```
[Find pods in Completed state]
  Delete job pods after 7 days
  ↓
[Remove old PVCs]
  Delete unbound persistent volumes
  ↓
[Remove old images]
  Clean up unused container images
  ↓
[Log cleanup activity]
```

## Best Practices

### 1. Authentication & Authorization

- Use RBAC (Role-Based Access Control)
- Create minimal-permission service accounts
- Rotate API tokens regularly
- Use network policies to restrict traffic

### 2. Monitoring

- Set up prometheus for metrics
- Create alerts for pod failures
- Monitor resource usage trends
- Track deployment success rate

### 3. Testing

- Test on staging cluster first
- Validate manifests before applying
- Run health checks after deployments
- Keep canary deployments for risky changes

### 4. Security

- Use private container registries
- Scan images for vulnerabilities
- Implement network policies
- Use secrets management (Sealed Secrets, Vault)

## Related Documentation

- [Edge Computing Guide](./edge-computing.md) — K8s at edge
- [Security Best Practices](../security-best-practices.md) — K8s security
- [Deployment Guide](../deployment-guide.md) — Production K8s
- [CI/CD Setup](../ci-cd-setup.md) — Automated K8s deployment
