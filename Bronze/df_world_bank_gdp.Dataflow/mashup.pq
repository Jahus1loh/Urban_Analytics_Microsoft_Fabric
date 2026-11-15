[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"], DestinationTypeSettings = [Kind = "Table"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[BindToDefaultDestination = true]
shared worldbank_gdp_usa = let
  Source = Json.Document(Web.Contents("https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=1000")),
  Data = Source{1},
  ToTable = Table.FromRecords(Data),
  ExpandCountry = Table.ExpandRecordColumn(ToTable, "country", {"id", "value"}, {"country_id", "country_name"}),
  ExpandIndicator = Table.ExpandRecordColumn(ExpandCountry, "indicator", {"id", "value"}, {"indicator_id", "indicator_name"}),
  Typed = Table.TransformColumnTypes(ExpandIndicator, {{"date", Int64.Type}, {"value", type number}, {"country_id", type text}, {"country_name", type text}, {"countryiso3code", type text}, {"indicator_id", type text}, {"indicator_name", type text}, {"unit", type text}, {"obs_status", type text}, {"decimal", Int64.Type}}),
  Ingested = DateTimeZone.UtcNow(),
  WithMeta = Table.AddColumn(Typed, "_ingested_at", each Ingested, type datetimezone)
in
  WithMeta;
shared DefaultDestination = let
  Source = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  #"Navigation 1" = Source{[workspaceId = "98b6d407-d99a-48f1-a048-6cacdf7adf6c"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[lakehouseId = "aeec20e2-163c-44e8-8987-c37faf72dd95"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[Id = "dbo", ItemKind = "Schema"]}[Data]
in
  #"Navigation 3";
