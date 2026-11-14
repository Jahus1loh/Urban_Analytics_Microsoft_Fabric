[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"], DestinationTypeSettings = [Kind = "Table"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[BindToDefaultDestination = true]
shared worldbank_gdp_usa = let
  Source = Json.Document(Web.Contents("https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json&per_page=100")),
  Data = Source{1},
  ToTable = Table.FromRecords(Data),
  RenameColumns = Table.RenameColumns(ToTable, {{"date", "year"}, {"value", "GDP"}}),
  SelectColumns = Table.SelectColumns(RenameColumns, {"year", "GDP"}),
  ChangeTypes = Table.TransformColumnTypes(SelectColumns, {{"year", Int64.Type}, {"GDP", Int64.Type}})
in
  ChangeTypes;
shared DefaultDestination = let
  Source = Lakehouse.Contents([HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true, CreateNavigationProperties = false, EnableFolding = false]),
  #"Navigation 1" = Source{[workspaceId = "98b6d407-d99a-48f1-a048-6cacdf7adf6c"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[lakehouseId = "aeec20e2-163c-44e8-8987-c37faf72dd95"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[Id = "dbo", ItemKind = "Schema"]}[Data]
in
  #"Navigation 3";
