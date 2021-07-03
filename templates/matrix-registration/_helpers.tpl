{{/* vim: set filetype=mustache: */}}
{{/*
Shared secret for the Synapse Workers
*/}}
{{- define "matrix.registrationApi.sharedSecret" -}}
{{- if .Values.matrixRegistration.adminApiSharedSecret }}
{{- .Values.matrixRegistration.adminApiSharedSecret -}}
{{- else }}
{{- randAlphaNum 64 -}}
{{- end }}
{{- end -}}
