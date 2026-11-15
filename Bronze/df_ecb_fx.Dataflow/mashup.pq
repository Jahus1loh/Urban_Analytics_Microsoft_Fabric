[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"], DestinationTypeSettings = [Kind = "Table"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[BindToDefaultDestination = true]
shared ECB_daily_FX = let
  Source = Csv.Document(Web.Contents("https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?format=csvdata"), [Delimiter = ",", Columns = 32, Encoding = 65001]),
  PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
  Typed = Table.TransformColumnTypes(PromotedHeaders, {{"TIME_PERIOD", type date}, {"OBS_VALUE", type number}}),
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
