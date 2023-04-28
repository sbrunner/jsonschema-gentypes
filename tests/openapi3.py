"""
Automatically generated file from a JSON schema.
"""


from typing import Dict, List, Literal, TypedDict, Union

from typing_extensions import Required

ExtentWithUniformAdditionalDimensionsSchema = Union[
    "_ComponentsSchemasExtent",
    Dict[str, "_ExtentWithUniformAdditionalDimensionsSchemaAllof1Additionalproperties"],
]
"""
Extent with Uniform Additional Dimensions Schema.

The extent module only addresses spatial and temporal extents. This module extends extent by specifying how
intervals and crs properties can be used to specify additional geometries.

WARNING: PEP 544 does not support an Intersection type,
so `allOf` is interpreted as a `Union` for now.
See: https://github.com/camptocamp/jsonschema-gentypes/issues/8
"""


class OgcapiCollectionsCollectionidGet(TypedDict, total=False):
    """
    Description of request on path '/collections/{collectionId}', using method 'get'.

    Retrieve the description of a collection available from this service.
    """

    path: Required["OgcapiCollectionsCollectionidGetPath"]
    """ Required property """

    query: Required["OgcapiCollectionsCollectionidGetQuery"]
    """ Required property """

    request_body: Required["OgcapiCollectionsCollectionidGetRequestbody"]
    """ Required property """

    response: "OgcapiCollectionsCollectionidGetResponse"


class OgcapiCollectionsCollectionidGetPath(TypedDict, total=False):
    """
    Parameter type 'path' of request on path '/collections/{collectionId}', using method 'get'.

    Request summary:
    Retrieve the description of a collection available from this service.
    """

    collectionId: Required[str]
    """ Required property """


class OgcapiCollectionsCollectionidGetQuery(TypedDict, total=False):
    """
    Parameter type 'query' of request on path '/collections/{collectionId}', using method 'get'.

    Request summary:
    Retrieve the description of a collection available from this service.
    """

    f: "OgcapiCollectionsCollectionidGetQueryF"


OgcapiCollectionsCollectionidGetQueryF = Union[Literal["json"], Literal["html"]]
OGCAPICOLLECTIONSCOLLECTIONIDGETQUERYF_JSON: Literal["json"] = "json"
"""The values for the 'OgcapiCollectionsCollectionidGetQueryF' enum"""
OGCAPICOLLECTIONSCOLLECTIONIDGETQUERYF_HTML: Literal["html"] = "html"
"""The values for the 'OgcapiCollectionsCollectionidGetQueryF' enum"""


class OgcapiCollectionsCollectionidGetRequestbody(TypedDict, total=False):
    href: Required[str]
    """
    Supplies the URI to a remote resource (or resource fragment).

    example: http://data.example.com/buildings/123

    Required property
    """

    rel: Required[str]
    """
    The type or semantics of the relation.

    example: alternate

    Required property
    """

    type: str
    """
    A hint indicating what the media type of the result of dereferencing the link should be.

    example: application/geo+json
    """

    templated: bool
    """ This flag set to true if the link is a URL template. """

    varBase: str
    """
    A base path to retrieve semantic information about the variables used in URL template.

    example: /ogcapi/vars/
    """

    hreflang: str
    """
    A hint indicating what the language of the result of dereferencing the link should be.

    example: en
    """

    title: str
    """
    Used to label the destination of a link such that it can be used as a human-readable identifier.

    example: Trierer Strasse 70, 53115 Bonn
    """

    length: int


OgcapiCollectionsCollectionidGetResponse = Union["OgcapiCollectionsCollectionidGetResponse200"]


class OgcapiCollectionsCollectionidGetResponse200(TypedDict, total=False):
    id: Required[str]
    """
    identifier of the collection used, for example, in URIs

    example: dem

    Required property
    """

    title: str
    """
    human readable title of the collection

    example: Digital Elevation Model
    """

    description: str
    """
    a description of the data in the collection

    example: A Digital Elevation Model.
    """

    links: Required[List["_ComponentsSchemasLink"]]
    """ Required property """

    extent: "ExtentWithUniformAdditionalDimensionsSchema"
    itemType: str
    """
    indicator about the type of the items in the collection if the collection has an accessible /collections/{collectionId}/items endpoint

    default: unknown
    """

    crs: List[str]
    """
    the list of coordinate reference systems supported by the API; the first item is the default coordinate reference system

    default:
      - http://www.opengis.net/def/crs/OGC/1.3/CRS84
    """

    dataType: Union[
        "_Ogcapicollectionscollectionidgetresponse200DatatypeAllof0",
        Union[str, "_ComponentsSchemasDatatypeAnyof1"],
    ]
    """
    WARNING: PEP 544 does not support an Intersection type,
    so `allOf` is interpreted as a `Union` for now.
    See: https://github.com/camptocamp/jsonschema-gentypes/issues/8
    """

    geometryDimension: int
    """
    The geometry dimension of the features shown in this layer (0: points, 1: curves, 2: surfaces, 3: solids), unspecified: mixed or unknown

    minimum: 0
    maximum: 3
    """

    minScaleDenominator: Union[int, float]
    """ Minimum scale denominator for usage of the collection """

    maxScaleDenominator: Union[int, float]
    """ Maximum scale denominator for usage of the collection """

    minCellSize: Union[int, float]
    """ Minimum cell size for usage of the collection """

    maxCellSize: Union[int, float]
    """ Maximum cell size for usage of the collection """


_COMPONENTS_SCHEMAS_EXTENT_SPATIAL_CRS_DEFAULT = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
""" Default value of the field path 'components schemas extent spatial crs' """


_COMPONENTS_SCHEMAS_EXTENT_TEMPORAL_TRS_DEFAULT = "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
""" Default value of the field path 'components schemas extent temporal trs' """


_ComponentsSchemasDatatypeAnyof1 = Union[Literal["map"], Literal["vector"], Literal["coverage"]]
_COMPONENTSSCHEMASDATATYPEANYOF1_MAP: Literal["map"] = "map"
"""The values for the '_ComponentsSchemasDatatypeAnyof1' enum"""
_COMPONENTSSCHEMASDATATYPEANYOF1_VECTOR: Literal["vector"] = "vector"
"""The values for the '_ComponentsSchemasDatatypeAnyof1' enum"""
_COMPONENTSSCHEMASDATATYPEANYOF1_COVERAGE: Literal["coverage"] = "coverage"
"""The values for the '_ComponentsSchemasDatatypeAnyof1' enum"""


class _ComponentsSchemasExtent(TypedDict, total=False):
    """
    The extent of the data in the collection. In the Core only spatial and temporal
    extents are specified. Extensions may add additional members to represent other
    extents, for example, thermal or pressure ranges.

    The first item in the array describes the overall extent of
    the data. All subsequent items describe more precise extents,
    e.g., to identify clusters of data.
    Clients only interested in the overall extent will only need to
    access the first item in each array.
    """

    spatial: "_ComponentsSchemasExtentSpatial"
    temporal: "_ComponentsSchemasExtentTemporal"


class _ComponentsSchemasExtentSpatial(TypedDict, total=False):
    """The spatial extent of the data in the collection."""

    bbox: List["_ComponentsSchemasExtentSpatialBboxItem"]
    """
    One or more bounding boxes that describe the spatial extent of the dataset.
    In the Core only a single bounding box is supported.

    Extensions may support additional areas.
    The first bounding box describes the overall spatial
    extent of the data. All subsequent bounding boxes describe
    more precise bounding boxes, e.g., to identify clusters of data.
    Clients only interested in the overall spatial extent will
    only need to access the first item in each array.

    minItems: 1
    """

    crs: "_ComponentsSchemasExtentSpatialCrs"
    grid: List["_ComponentsSchemasExtentSpatialGridItem"]
    """
    Provides information about the limited availability of data within the collection organized
    as a grid (regular or irregular) along each spatial dimension.

    minItems: 2
    maxItems: 3
    """


_ComponentsSchemasExtentSpatialBboxItem = List[Union[int, float]]
"""
Each bounding box is provided as four or six numbers, depending on
whether the coordinate reference system includes a vertical axis
(height or depth):

* Lower left corner, coordinate axis 1
* Lower left corner, coordinate axis 2
* Minimum value, coordinate axis 3 (optional)
* Upper right corner, coordinate axis 1
* Upper right corner, coordinate axis 2
* Maximum value, coordinate axis 3 (optional)

If the value consists of four numbers, the coordinate reference system is
WGS 84 longitude/latitude (http://www.opengis.net/def/crs/OGC/1.3/CRS84)
unless a different coordinate reference system is specified in a parameter `bbox-crs`.

If the value consists of six numbers, the coordinate reference system is WGS 84
longitude/latitude/ellipsoidal height (http://www.opengis.net/def/crs/OGC/0/CRS84h)
unless a different coordinate reference system is specified in a parameter `bbox-crs`.

For WGS 84 longitude/latitude the values are in most cases the sequence of
minimum longitude, minimum latitude, maximum longitude and maximum latitude.
However, in cases where the box spans the antimeridian the first value
(west-most box edge) is larger than the third value (east-most box edge).

If the vertical axis is included, the third and the sixth number are
the bottom and the top of the 3-dimensional bounding box.

If a feature has multiple spatial geometry properties, it is the decision of the
server whether only a single spatial geometry property is used to determine
the extent or all relevant geometries.
"""


_ComponentsSchemasExtentSpatialCrs = Union[
    Literal["http://www.opengis.net/def/crs/OGC/1.3/CRS84"],
    Literal["http://www.opengis.net/def/crs/OGC/0/CRS84h"],
]
"""
Coordinate reference system of the coordinates in the spatial extent
(property `bbox`). The default reference system is WGS 84 longitude/latitude.
In the Core the only other supported coordinate reference system is
WGS 84 longitude/latitude/ellipsoidal height for coordinates with height.
Extensions may support additional coordinate reference systems and add
additional enum values.

default: http://www.opengis.net/def/crs/OGC/1.3/CRS84
"""
_COMPONENTSSCHEMASEXTENTSPATIALCRS_HTTP_COLON__SOLIDUS__SOLIDUS_WWW_FULL_STOP_OPENGIS_FULL_STOP_NET_SOLIDUS_DEF_SOLIDUS_CRS_SOLIDUS_OGC_SOLIDUS_1_FULL_STOP_3_SOLIDUS_CRS84: Literal[
    "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
] = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
"""The values for the 'Coordinate reference system of the coordinates in the spatial extent' enum"""
_COMPONENTSSCHEMASEXTENTSPATIALCRS_HTTP_COLON__SOLIDUS__SOLIDUS_WWW_FULL_STOP_OPENGIS_FULL_STOP_NET_SOLIDUS_DEF_SOLIDUS_CRS_SOLIDUS_OGC_SOLIDUS_0_SOLIDUS_CRS84H: Literal[
    "http://www.opengis.net/def/crs/OGC/0/CRS84h"
] = "http://www.opengis.net/def/crs/OGC/0/CRS84h"
"""The values for the 'Coordinate reference system of the coordinates in the spatial extent' enum"""


class _ComponentsSchemasExtentSpatialGridItem(TypedDict, total=False):
    coordinates: List["_ComponentsSchemasExtentSpatialGridItemCoordinatesItem"]
    """
    List of coordinates along the dimension for which data organized as an irregular grid in the collection is available
    (e.g., 2, 10, 80, 100).

    minItems: 1
    """

    cellsCount: int
    """
    Number of samples available along the dimension for data organized as a regular grid.
    For values representing the whole area of contiguous cells spanning _resolution_ units along the dimension, this will be (_upperBound_ - _lowerBound_) / _resolution_.
    For values representing infinitely small point cells spaced by _resolution_ units along the dimension, this will be (_upperBound_ - _lowerBound_) / _resolution_ + 1.

    example: 50
    """

    resolution: Union["_ComponentsSchemasExtentSpatialGridItemResolutionOneof0", Union[int, float]]
    """
    Resolution of regularly gridded data along the dimension in the collection

    example: 0.0006866455078

    oneOf
    """


_ComponentsSchemasExtentSpatialGridItemCoordinatesItem = Union[
    "_ComponentsSchemasExtentSpatialGridItemCoordinatesItemOneof0", Union[int, float]
]
""" oneOf """


_ComponentsSchemasExtentSpatialGridItemCoordinatesItemOneof0 = str
""" nullable: True """


_ComponentsSchemasExtentSpatialGridItemResolutionOneof0 = str
""" nullable: True """


class _ComponentsSchemasExtentTemporal(TypedDict, total=False):
    """The temporal extent of the features in the collection."""

    interval: List["_ComponentsSchemasExtentTemporalIntervalItem"]
    """
    One or more time intervals that describe the temporal extent of the dataset.
    In the Core only a single time interval is supported.

    Extensions may support multiple intervals.
    The first time interval describes the overall
    temporal extent of the data. All subsequent time intervals describe
    more precise time intervals, e.g., to identify clusters of data.
    Clients only interested in the overall extent will only need
    to access the first item in each array.

    minItems: 1
    """

    trs: "_ComponentsSchemasExtentTemporalTrs"
    grid: "_ComponentsSchemasExtentTemporalGrid"


class _ComponentsSchemasExtentTemporalGrid(TypedDict, total=False):
    """Provides information about the limited availability of data within the collection organized as a grid (regular or irregular) along the temporal dimension."""

    coordinates: List["_ComponentsSchemasExtentTemporalGridCoordinatesItem"]
    """
    List of coordinates along the temporal dimension for which data organized as an irregular grid in the collection is available
    (e.g., "2017-11-14T09:00Z","2017-11-14T12:00Z","2017-11-14T15:00Z","2017-11-14T18:00Z","2017-11-14T21:00Z").

    minItems: 1
    """

    cellsCount: int
    """
    Number of samples available along the temporal dimension for data organized as a regular grid.
    For values representing the whole area of contiguous cells spanning _resolution_ units along the dimension, this will be (_upperBound_ - _lowerBound_) / _resolution_.
    For values representing infinitely small point cells spaced by _resolution_ units along the dimension, this will be (_upperBound_ - _lowerBound_) / _resolution_ + 1.

    example: 50
    """

    resolution: Union["_ComponentsSchemasExtentTemporalGridResolutionOneof0", Union[int, float]]
    """
    Resolution of regularly gridded data along the temporal dimension in the collection

    example: PT1H

    oneOf
    """


_ComponentsSchemasExtentTemporalGridCoordinatesItem = str
""" nullable: True """


_ComponentsSchemasExtentTemporalGridResolutionOneof0 = str
""" nullable: True """


_ComponentsSchemasExtentTemporalIntervalItem = List["_ComponentsSchemasExtentTemporalIntervalItemItem"]
"""
Begin and end times of the time interval. The timestamps are in the
temporal coordinate reference system specified in `trs`. By default
this is the Gregorian calendar.

The value `null` for start or end time is supported and indicates a half-bounded time interval.

minItems: 2
maxItems: 2
"""


_ComponentsSchemasExtentTemporalIntervalItemItem = str
"""
format: date-time
nullable: True
"""


_ComponentsSchemasExtentTemporalTrs = Union[Literal["http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"]]
"""
Coordinate reference system of the coordinates in the temporal extent
(property `interval`). The default reference system is the Gregorian calendar.
In the Core this is the only supported temporal coordinate reference system.
Extensions may support additional temporal coordinate reference systems and add
additional enum values.

default: http://www.opengis.net/def/uom/ISO-8601/0/Gregorian
"""
_COMPONENTSSCHEMASEXTENTTEMPORALTRS_HTTP_COLON__SOLIDUS__SOLIDUS_WWW_FULL_STOP_OPENGIS_FULL_STOP_NET_SOLIDUS_DEF_SOLIDUS_UOM_SOLIDUS_ISO_8601_SOLIDUS_0_SOLIDUS_GREGORIAN: Literal[
    "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
] = "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
"""The values for the 'Coordinate reference system of the coordinates in the temporal extent' enum"""


class _ComponentsSchemasLink(TypedDict, total=False):
    href: Required[str]
    """
    Supplies the URI to a remote resource (or resource fragment).

    example: http://data.example.com/buildings/123

    Required property
    """

    rel: Required[str]
    """
    The type or semantics of the relation.

    example: alternate

    Required property
    """

    type: str
    """
    A hint indicating what the media type of the result of dereferencing the link should be.

    example: application/geo+json
    """

    templated: bool
    """ This flag set to true if the link is a URL template. """

    varBase: str
    """
    A base path to retrieve semantic information about the variables used in URL template.

    example: /ogcapi/vars/
    """

    hreflang: str
    """
    A hint indicating what the language of the result of dereferencing the link should be.

    example: en
    """

    title: str
    """
    Used to label the destination of a link such that it can be used as a human-readable identifier.

    example: Trierer Strasse 70, 53115 Bonn
    """

    length: int


class _ExtentWithUniformAdditionalDimensionsSchemaAllof1Additionalproperties(TypedDict, total=False):
    """The domain intervals for any additional dimensions of the extent (envelope) beyond those described in temporal and spatial."""

    interval: List["_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesIntervalItem"]
    """
    One or more intervals that describe the extent for this dimension of the dataset.
    The value `null` is supported and indicates an unbounded or half-bounded interval.
    The first interval describes the overall extent of the data for this dimension.
    All subsequent intervals describe more precise intervals, e.g., to identify clusters of data.
    Clients only interested in the overall extent will only need
    to access the first item (a pair of lower and upper bound values).

    minItems: 1
    """

    crs: str
    """ generic coordinate reference system suitable for any type of dimensions """

    trs: str
    """ temporal coordinate reference system (e.g. as defined by Features for 'temporal') """

    vrs: str
    """ vertical coordinate reference system (e.g. as defined in EDR for 'vertical') """

    grid: "_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesGrid"


class _ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesGrid(TypedDict, total=False):
    """Provides information about the limited availability of data within the collection organized as a grid (regular or irregular) along the dimension."""

    coordinates: List[
        "_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesGridCoordinatesItem"
    ]
    """
    List of coordinates along the temporal dimension for which data organized as an irregular grid in the collection is available
    (e.g., 2, 10, 80, 100).

    minItems: 1
    """

    cellsCount: int
    """
    Number of samples available along the dimension for data organized as a regular grid.
    For values representing the whole area of contiguous cells spanning _resolution_ units along the dimension, this will be (_upperBound_ - _lowerBound_) / _resolution_.
    For values representing infinitely small point cells spaced by _resolution_ units along the dimension, this will be (_upperBound_ - _lowerBound_) / _resolution_ + 1.

    example: 50
    """

    resolution: Union[
        "_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesGridResolutionOneof0",
        Union[int, float],
    ]
    """
    Resolution of regularly gridded data along the dimension in the collection

    oneOf
    """


_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesGridCoordinatesItem = Union[
    "_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesGridCoordinatesItemOneof0",
    Union[int, float],
]
""" oneOf """


_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesGridCoordinatesItemOneof0 = str
""" nullable: True """


_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesGridResolutionOneof0 = str
""" nullable: True """


_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesIntervalItem = List[
    "_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesIntervalItemItem"
]
"""
Lower and upper bound values of the interval. The values
are in the coordinate reference system specified in `crs`, `trs` or `vrs`.

minItems: 2
maxItems: 2
"""


_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesIntervalItemItem = Union[
    "_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesIntervalItemItemOneof0",
    Union[int, float],
]
""" oneOf """


_ExtentWithUniformAdditionalDimensionsSchemaAllof1AdditionalpropertiesIntervalItemItemOneof0 = str
""" nullable: True """


_OGCAPICOLLECTIONSCOLLECTIONIDGETRESPONSE200_CRS_DEFAULT = ["http://www.opengis.net/def/crs/OGC/1.3/CRS84"]
""" Default value of the field path 'OgcapiCollectionsCollectionidGetResponse200 crs' """


_OGCAPICOLLECTIONSCOLLECTIONIDGETRESPONSE200_ITEMTYPE_DEFAULT = "unknown"
""" Default value of the field path 'OgcapiCollectionsCollectionidGetResponse200 itemType' """


_Ogcapicollectionscollectionidgetresponse200DatatypeAllof0 = Any
"""
Type of data represented in the collection

WARNING: we get an schema without any type
"""
