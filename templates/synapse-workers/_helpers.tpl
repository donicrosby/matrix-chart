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
