"""
Automatically generated file from a JSON schema.
"""

from typing import Any, Literal, TypedDict, Union

from typing_extensions import Required


class OpenAPI(TypedDict, total=False):
    """
    The description of OpenAPI v3.1.x Documents without Schema Object validation

    anyOf:
      - required:
        - paths
      - required:
        - components
      - required:
        - webhooks
    unevaluatedProperties: False
    """

    openapi: Required[str]
    r"""
    pattern: ^3\.1\.\d+(-.+)?$

    Required property
    """

    info: Required["_Info"]
    """
    $comment: https://spec.openapis.org/oas/v3.1#info-object
    unevaluatedProperties: False

    Required property
    """

    jsonSchemaDialect: str
    """
    format: uri-reference
    default: https://spec.openapis.org/oas/3.1/dialect/2024-11-10
    """

    servers: list["_Server"]
    """
    default:
      - url: /
    """

    paths: "_Paths"
    """
    $comment: https://spec.openapis.org/oas/v3.1#paths-object
    unevaluatedProperties: False
    """

    webhooks: dict[str, "_PathItem"]
    components: "_Components"
    """
    $comment: https://spec.openapis.org/oas/v3.1#components-object
    unevaluatedProperties: False
    """

    security: list["_SecurityRequirement"]
    tags: list["_Tag"]
    externalDocs: "_ExternalDocumentation"
    """
    $comment: https://spec.openapis.org/oas/v3.1#external-documentation-object
    unevaluatedProperties: False
    """


_Callbacks = dict[str, "_PathItem"]
""" $comment: https://spec.openapis.org/oas/v3.1#callback-object """


class _Components(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#components-object
    unevaluatedProperties: False
    """

    responses: dict[str, "_Response"]
    parameters: dict[str, "_Parameter"]
    examples: dict[str, "_Example"]
    requestBodies: dict[str, "_RequestBody"]
    headers: dict[str, "_Header"]
    securitySchemes: dict[str, "_SecurityScheme"]
    links: dict[str, "_Link"]
    callbacks: dict[str, "_Callbacks"]
    pathItems: dict[str, "_PathItem"]


class _Contact(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#contact-object
    unevaluatedProperties: False
    """

    name: str
    url: str
    """ format: uri-reference """

    email: str
    """ format: email """


_Content = dict[str, "_MediaType"]
"""
$comment: https://spec.openapis.org/oas/v3.1#fixed-fields-10
propertyNames:
  format: media-range
"""


_ENCODING_ALLOWRESERVED_DEFAULT = False
""" Default value of the field path 'encoding allowReserved' """


_ENCODING_STYLE_DEFAULT = "form"
""" Default value of the field path 'encoding style' """


class _Encoding(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#encoding-object
    allOf:
      - $ref: '#/$defs/styles-for-form'
    unevaluatedProperties: False
    """

    contentType: str
    """ format: media-range """

    headers: dict[str, "_Header"]
    style: "_EncodingStyle"
    """ default: form """

    explode: bool
    allowReserved: bool
    """ default: False """


_EncodingStyle = Literal["form", "spaceDelimited", "pipeDelimited", "deepObject"]
""" default: form """
_ENCODINGSTYLE_FORM: Literal["form"] = "form"
"""The values for the 'default: form' enum"""
_ENCODINGSTYLE_SPACEDELIMITED: Literal["spaceDelimited"] = "spaceDelimited"
"""The values for the 'default: form' enum"""
_ENCODINGSTYLE_PIPEDELIMITED: Literal["pipeDelimited"] = "pipeDelimited"
"""The values for the 'default: form' enum"""
_ENCODINGSTYLE_DEEPOBJECT: Literal["deepObject"] = "deepObject"
"""The values for the 'default: form' enum"""


class _Example(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#example-object
    not:
      required:
      - value
      - externalValue
    unevaluatedProperties: False
    """

    summary: str
    description: str
    value: Any
    externalValue: str
    """ format: uri-reference """


class _ExternalDocumentation(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#external-documentation-object
    unevaluatedProperties: False
    """

    description: str
    url: Required[str]
    """
    format: uri-reference

    Required property
    """


_HEADER_DEPRECATED_DEFAULT = False
""" Default value of the field path 'header deprecated' """


_HEADER_REQUIRED_DEFAULT = False
""" Default value of the field path 'header required' """


class _Header(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#header-object
    oneOf:
      - required:
        - schema
      - required:
        - content
    dependentSchemas:
      schema:
        $ref: '#/$defs/examples'
        properties:
          explode:
            default: false
            type: boolean
          style:
            const: simple
            default: simple
    unevaluatedProperties: False
    """

    description: str
    required: bool
    """ default: False """

    deprecated: bool
    """ default: False """

    content: "_Content"
    """
    $comment: https://spec.openapis.org/oas/v3.1#fixed-fields-10
    propertyNames:
      format: media-range
    """


class _Info(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#info-object
    unevaluatedProperties: False
    """

    title: Required[str]
    """ Required property """

    summary: str
    description: str
    termsOfService: str
    """ format: uri-reference """

    contact: "_Contact"
    """
    $comment: https://spec.openapis.org/oas/v3.1#contact-object
    unevaluatedProperties: False
    """

    license: "_License"
    """
    $comment: https://spec.openapis.org/oas/v3.1#license-object
    dependentSchemas:
      identifier:
        not:
          required:
          - url
    unevaluatedProperties: False
    """

    version: Required[str]
    """ Required property """


class _License(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#license-object
    dependentSchemas:
      identifier:
        not:
          required:
          - url
    unevaluatedProperties: False
    """

    name: Required[str]
    """ Required property """

    identifier: str
    url: str
    """ format: uri-reference """


class _Link(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#link-object
    oneOf:
      - required:
        - operationRef
      - required:
        - operationId
    unevaluatedProperties: False
    """

    operationRef: str
    """ format: uri-reference """

    operationId: str
    parameters: dict[str, str]
    requestBody: Any
    description: str
    body: "_Server"
    """
    $comment: https://spec.openapis.org/oas/v3.1#server-object
    unevaluatedProperties: False
    """


class _MediaType(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#media-type-object
    unevaluatedProperties: False
    """

    encoding: dict[str, "_Encoding"]
    example: Any
    examples: dict[str, "_Example"]


_OPENAPI_JSONSCHEMADIALECT_DEFAULT = "https://spec.openapis.org/oas/3.1/dialect/2024-11-10"
""" Default value of the field path 'OpenAPI jsonSchemaDialect' """


_OPENAPI_SERVERS_DEFAULT = [{"url": "/"}]
""" Default value of the field path 'OpenAPI servers' """


_OPERATION_DEPRECATED_DEFAULT = False
""" Default value of the field path 'operation deprecated' """


class _Operation(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#operation-object
    unevaluatedProperties: False
    """

    tags: list[str]
    summary: str
    description: str
    externalDocs: "_ExternalDocumentation"
    """
    $comment: https://spec.openapis.org/oas/v3.1#external-documentation-object
    unevaluatedProperties: False
    """

    operationId: str
    parameters: list["_Parameter"]
    requestBody: "_RequestBody"
    """
    $comment: https://spec.openapis.org/oas/v3.1#request-body-object
    unevaluatedProperties: False
    """

    responses: "_Responses"
    """
    $comment: https://spec.openapis.org/oas/v3.1#responses-object
    minProperties: 1
    unevaluatedProperties: False


    WARNING: Normally the types should be a mix of each other instead of Union.
    See: https://github.com/camptocamp/jsonschema-gentypes/issues/7
    """

    callbacks: dict[str, "_Callbacks"]
    deprecated: bool
    """ default: False """

    security: list["_SecurityRequirement"]
    servers: list["_Server"]


_PARAMETER_DEPRECATED_DEFAULT = False
""" Default value of the field path 'parameter deprecated' """


_PARAMETER_REQUIRED_DEFAULT = False
""" Default value of the field path 'parameter required' """


# | $comment: https://spec.openapis.org/oas/v3.1#parameter-object
# | oneOf:
# |   - required:
# |     - schema
# |   - required:
# |     - content
# | dependentSchemas:
# |   schema:
# |     $defs:
# |       styles-for-cookie:
# |         if:
# |           properties:
# |             in:
# |               const: cookie
# |           required:
# |           - in
# |         then:
# |           properties:
# |             style:
# |               const: form
# |               default: form
# |       styles-for-header:
# |         if:
# |           properties:
# |             in:
# |               const: header
# |           required:
# |           - in
# |         then:
# |           properties:
# |             style:
# |               const: simple
# |               default: simple
# |       styles-for-path:
# |         if:
# |           properties:
# |             in:
# |               const: path
# |           required:
# |           - in
# |         then:
# |           properties:
# |             required:
# |               const: true
# |             style:
# |               default: simple
# |               enum:
# |               - matrix
# |               - label
# |               - simple
# |           required:
# |           - required
# |       styles-for-query:
# |         if:
# |           properties:
# |             in:
# |               const: query
# |           required:
# |           - in
# |         then:
# |           properties:
# |             allowReserved:
# |               default: false
# |               type: boolean
# |             style:
# |               default: form
# |               enum:
# |               - form
# |               - spaceDelimited
# |               - pipeDelimited
# |               - deepObject
# |     allOf:
# |     - $ref: '#/$defs/examples'
# |     - $ref: '#/$defs/parameter/dependentSchemas/schema/$defs/styles-for-path'
# |     - $ref: '#/$defs/parameter/dependentSchemas/schema/$defs/styles-for-header'
# |     - $ref: '#/$defs/parameter/dependentSchemas/schema/$defs/styles-for-query'
# |     - $ref: '#/$defs/parameter/dependentSchemas/schema/$defs/styles-for-cookie'
# |     - $ref: '#/$defs/styles-for-form'
# |     properties:
# |       explode:
# |         type: boolean
# |       style:
# |         type: string
# | unevaluatedProperties: False
_Parameter = TypedDict(
    "_Parameter",
    {
        # | Required property
        "name": Required[str],
        # | Required property
        "in": Required["_ParameterIn"],
        "description": str,
        # | default: False
        "required": bool,
        # | default: False
        "deprecated": bool,
        # | $comment: https://spec.openapis.org/oas/v3.1#fixed-fields-10
        # | propertyNames:
        # |   format: media-range
        "content": "_Content",
    },
    total=False,
)


_ParameterIn = Literal["query", "header", "path", "cookie"]
_PARAMETERIN_QUERY: Literal["query"] = "query"
"""The values for the '_ParameterIn' enum"""
_PARAMETERIN_HEADER: Literal["header"] = "header"
"""The values for the '_ParameterIn' enum"""
_PARAMETERIN_PATH: Literal["path"] = "path"
"""The values for the '_ParameterIn' enum"""
_PARAMETERIN_COOKIE: Literal["cookie"] = "cookie"
"""The values for the '_ParameterIn' enum"""


# | $comment: https://spec.openapis.org/oas/v3.1#path-item-object
# | unevaluatedProperties: False
_PathItem = TypedDict(
    "_PathItem",
    {
        # | format: uri-reference
        "$ref": str,
        "summary": str,
        "description": str,
        "servers": list["_Server"],
        "parameters": list["_Parameter"],
        # | $comment: https://spec.openapis.org/oas/v3.1#operation-object
        # | unevaluatedProperties: False
        "get": "_Operation",
        # | $comment: https://spec.openapis.org/oas/v3.1#operation-object
        # | unevaluatedProperties: False
        "put": "_Operation",
        # | $comment: https://spec.openapis.org/oas/v3.1#operation-object
        # | unevaluatedProperties: False
        "post": "_Operation",
        # | $comment: https://spec.openapis.org/oas/v3.1#operation-object
        # | unevaluatedProperties: False
        "delete": "_Operation",
        # | $comment: https://spec.openapis.org/oas/v3.1#operation-object
        # | unevaluatedProperties: False
        "options": "_Operation",
        # | $comment: https://spec.openapis.org/oas/v3.1#operation-object
        # | unevaluatedProperties: False
        "head": "_Operation",
        # | $comment: https://spec.openapis.org/oas/v3.1#operation-object
        # | unevaluatedProperties: False
        "patch": "_Operation",
        # | $comment: https://spec.openapis.org/oas/v3.1#operation-object
        # | unevaluatedProperties: False
        "trace": "_Operation",
    },
    total=False,
)


_Paths = dict[str, "_PathItem"]
"""
$comment: https://spec.openapis.org/oas/v3.1#paths-object
unevaluatedProperties: False
"""


_REQUEST_BODY_REQUIRED_DEFAULT = False
""" Default value of the field path 'request-body required' """


class _RequestBody(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#request-body-object
    unevaluatedProperties: False
    """

    description: str
    content: Required["_Content"]
    """
    $comment: https://spec.openapis.org/oas/v3.1#fixed-fields-10
    propertyNames:
      format: media-range

    Required property
    """

    required: bool
    """ default: False """


class _Response(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#response-object
    unevaluatedProperties: False
    """

    description: Required[str]
    """ Required property """

    headers: dict[str, "_Header"]
    content: "_Content"
    """
    $comment: https://spec.openapis.org/oas/v3.1#fixed-fields-10
    propertyNames:
      format: media-range
    """

    links: dict[str, "_Link"]


_Responses = Union[dict[str, "_Response"], "_ResponsesTyped"]
"""
$comment: https://spec.openapis.org/oas/v3.1#responses-object
minProperties: 1
unevaluatedProperties: False


WARNING: Normally the types should be a mix of each other instead of Union.
See: https://github.com/camptocamp/jsonschema-gentypes/issues/7
"""


class _ResponsesTyped(TypedDict, total=False):
    default: "_Response"
    """
    $comment: https://spec.openapis.org/oas/v3.1#response-object
    unevaluatedProperties: False
    """


_SecurityRequirement = dict[str, list[str]]
""" $comment: https://spec.openapis.org/oas/v3.1#security-requirement-object """


class _SecurityScheme(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#security-scheme-object
    allOf:
      - $ref: '#/$defs/security-scheme/$defs/type-apikey'
      - $ref: '#/$defs/security-scheme/$defs/type-http'
      - $ref: '#/$defs/security-scheme/$defs/type-http-bearer'
      - $ref: '#/$defs/security-scheme/$defs/type-oauth2'
      - $ref: '#/$defs/security-scheme/$defs/type-oidc'
    unevaluatedProperties: False
    """

    type: Required["_SecuritySchemeType"]
    """ Required property """

    description: str


_SecuritySchemeType = Literal["apiKey", "http", "mutualTLS", "oauth2", "openIdConnect"]
_SECURITYSCHEMETYPE_APIKEY: Literal["apiKey"] = "apiKey"
"""The values for the '_SecuritySchemeType' enum"""
_SECURITYSCHEMETYPE_HTTP: Literal["http"] = "http"
"""The values for the '_SecuritySchemeType' enum"""
_SECURITYSCHEMETYPE_MUTUALTLS: Literal["mutualTLS"] = "mutualTLS"
"""The values for the '_SecuritySchemeType' enum"""
_SECURITYSCHEMETYPE_OAUTH2: Literal["oauth2"] = "oauth2"
"""The values for the '_SecuritySchemeType' enum"""
_SECURITYSCHEMETYPE_OPENIDCONNECT: Literal["openIdConnect"] = "openIdConnect"
"""The values for the '_SecuritySchemeType' enum"""


class _Server(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#server-object
    unevaluatedProperties: False
    """

    url: Required[str]
    """ Required property """

    description: str
    variables: dict[str, "_ServerVariable"]


class _ServerVariable(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#server-variable-object
    unevaluatedProperties: False
    """

    enum: list[str]
    """ minItems: 1 """

    default: Required[str]
    """ Required property """

    description: str


class _Tag(TypedDict, total=False):
    """
    $comment: https://spec.openapis.org/oas/v3.1#tag-object
    unevaluatedProperties: False
    """

    name: Required[str]
    """ Required property """

    description: str
    externalDocs: "_ExternalDocumentation"
    """
    $comment: https://spec.openapis.org/oas/v3.1#external-documentation-object
    unevaluatedProperties: False
    """
