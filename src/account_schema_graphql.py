account_schema_graphql = """
schema {
  query: Query
}
type Account {
  id: Int!
  number: String!
  isActive: Boolean!
  type: AccountType!
  customerId: Int!
  customer: Customer!
}
type AccountsConnection {
  pageInfo: PageInfo!
  edges: [AccountsEdge!]
  nodes: [Account!]
  totalCount: Int! 
}
type AccountsEdge {
  cursor: String!
  node: Account!
}
type Customer {
  accounts(
    first: Int
    after: String
    last: Int
    before: String
    where: AccountFilterInput 
    order: [AccountSortInput!] 
  ): AccountsConnection
  id: Int!
  name: String!
  identityNumber: Int!
  age: Int!
}
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
type Query {
  accounts(
    first: Int
    after: String
    last: Int
    before: String
    where: AccountFilterInput 
    order: [AccountSortInput!] 
  ): AccountsConnection
}
input AccountFilterInput {
  and: [AccountFilterInput!]
  or: [AccountFilterInput!]
  id: IntOperationFilterInput
  number: StringOperationFilterInput
  isActive: BooleanOperationFilterInput
  type: AccountTypeOperationFilterInput
  customerId: IntOperationFilterInput
  customer: CustomerFilterInput
}
input AccountSortInput {
  id: SortEnumType 
  number: SortEnumType 
  isActive: SortEnumType 
  type: SortEnumType 
  customerId: SortEnumType 
  customer: CustomerSortInput 
}
input AccountTypeOperationFilterInput {
  eq: AccountType 
  neq: AccountType 
  in: [AccountType!] 
  nin: [AccountType!] 
}
input BooleanOperationFilterInput {
  eq: Boolean 
  neq: Boolean 
}
input CustomerFilterInput {
  and: [CustomerFilterInput!]
  or: [CustomerFilterInput!]
  id: IntOperationFilterInput
  name: StringOperationFilterInput
  identityNumber: IntOperationFilterInput
  age: IntOperationFilterInput
}
input CustomerSortInput {
  id: SortEnumType 
  name: SortEnumType 
  identityNumber: SortEnumType 
  age: SortEnumType 
}
input IntOperationFilterInput {
  eq: Int 
  neq: Int 
  in: [Int] 
  nin: [Int] 
  gt: Int 
  ngt: Int 
  gte: Int 
  ngte: Int 
  lt: Int 
  nlt: Int 
  lte: Int 
  nlte: Int 
}
input StringOperationFilterInput {
  and: [StringOperationFilterInput!]
  or: [StringOperationFilterInput!]
  eq: String 
  neq: String 
  contains: String 
  ncontains: String 
  in: [String] 
  nin: [String] 
  startsWith: String 
  nstartsWith: String 
  endsWith: String 
  nendsWith: String 
}
enum AccountType {
  DOMESTIC
  COMMERCIAL
}
enum SortEnumType {
  ASC
  DESC
}

"""

escaped_account_schema_graphql = account_schema_graphql.replace("{", "{{").replace("}", "}}")