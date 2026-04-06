class EnvVariableHandler:
    """Base class for collecting environment variables to inject into the build process."""

    def validate(self, variables):
        return None


class StaticEnvVariableHandler(EnvVariableHandler):
    """Collects environment variables with static/hardcoded values for injection into the build process."""

    def __init__(self, value):
        self.value = value

    def get_value(self, variables):
        return self.value


class FieldEnvVariableHandler(EnvVariableHandler):
    """Collects environment variables from fields in the request sent to the web server for injection into the build process."""

    def __init__(self, fieldname):
        self.fieldname = fieldname

    def get_value(self, variables):
        return variables[self.fieldname]

    def validate(self, variables):
        if self.fieldname in variables:
            return None
        return f"Missing field {self.fieldname}"


class EnvironmentVariable:
    """Represents an environment variable to be injected into the build process.

    Collects values from either static configuration or GET request fields based on manifest settings.
    """

    def __init__(self, name, schema):
        self.name = name
        self.source = schema.source
        self.fieldname = schema.fieldname
        self.value = schema.value

        match self.source:
            case "field":
                self.handler = FieldEnvVariableHandler(self.fieldname)
            case "static":
                self.handler = StaticEnvVariableHandler(self.value)

    def get_value(self, variables):
        return self.handler.get_value(variables)

    def validate(self, variables):
        result = self.handler.validate(variables)
        if result is None:
            return None
        return f"Environment variable {self.name}: {result}"
