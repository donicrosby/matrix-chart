{{/* vim: set filetype=mustache: */}}
{{/*
Shared secret for the Synapse Workers
*/}}
{{- define "matrix.synapseWorkers.sharedSecret" -}}
{{- if .Values.synapseWorkers.sharedSecret }}
{{- .Values.synapseWorkers.sharedSecret -}}
{{- else }}
{{- randAlphaNum 64 -}}
{{- end }}
{{- end -}}

{{/*
Deterine if client workers should be pointed to a single combined deployment
or multiple deployments
*/}}
{{- define "matrix.synapseWorkers.clientWorkers" -}}
{{- if .Values.synapseWorkers.separate }}
{{- printf "%s-%s" (include "matrix.name" .) "synapse-client-workers" -}}
{{- else }}
{{- printf "%s-%s" (include "matrix.name" .) "synapse-generic-workers" -}}
{{- end }}
{{- end -}}

{{/*
Deterine if federation workers should be pointed to a single combined deployment
or multiple deployments
*/}}
{{- define "matrix.synapseWorkers.federationWorkers" -}}
{{- if .Values.synapseWorkers.separate }}
{{- printf "%s-%s" (include "matrix.name" .) "synapse-fedneration-workers" -}}
{{- else }}
{{- printf "%s-%s" (include "matrix.name" .) "synapse-generic-workers" -}}
{{- end }}
{{- end -}}
