# input

Configures environment variables and files to inject into the build container. Both are populated from either static values or fields in the job request JSON body.

The entire `input` section is optional. If omitted, the build runs with no injected variables or files.

```yaml
build:
  # [...]
input:
  environment:
    MY_VAR:
      source: field
      fieldname: my_var
    STATIC_VAR:
      source: static
      value: "hello"
  files:
    - fieldname: config_data
      destination: config.json
output:
  # [...]
```

## environment

A map of environment variable names to their source configuration.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source` | string | Yes | `field` or `static` |
| `fieldname` | string | When source is `field` | Key in the job request JSON to read the value from |
| `value` | string | When source is `static` | Hardcoded value for the variable |

### source: field

The value is read from the job request JSON body at runtime. Validation ensures the field is present before the job starts.

### source: static

The value is set directly in the manifest and does not depend on the request.

## files

A list of files to write into the build workdir before running. Each file's content is read from a field in the job request JSON.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `fieldname` | string | Yes | Key in the job request JSON containing the file content |
| `destination` | string | Yes | Path relative to the workdir where the file is written |
