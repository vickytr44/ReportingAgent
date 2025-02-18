customer_schema_graphql = """
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
type Customer {
  id: Int!
  name: String!
  identityNumber: Int!
  age: Int!
  accounts(
    where: AccountFilterInput 
    order: [AccountSortInput!] 
  ): [Account!]!
}
type CustomersConnection {
  pageInfo: PageInfo!
  edges: [CustomersEdge!]
  nodes: [Customer!]
  totalCount: Int! 
}
type CustomersEdge {
  cursor: String!
  node: Customer!
}
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
type Query {
  customers(
    first: Int
    after: String
    last: Int
    before: String
    where: CustomerFilterInput 
    order: [CustomerSortInput!] 
  ): CustomersConnection
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
  accounts: ListFilterInputTypeOfAccountFilterInput
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
input ListFilterInputTypeOfAccountFilterInput {
  all: AccountFilterInput 
  none: AccountFilterInput 
  some: AccountFilterInput 
  any: Boolean 
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

escaped_customer_schema_graphql = customer_schema_graphql.replace("{", "{{").replace("}", "}}")