# How to call api using graphql 
* creating New user 
1-``` mutation{
  createUser(name:"Ali", email:"a@a.com", password:"123") 
  { 
  id 
  name 
  email }
  }
  ```
* creating New Blog 


* Creating blog 
``` mutation {
  updateBlog(
    id: 1
    title: "New Title1"
    published :true
  ) {
    id
    title
    body
    published
  }
}
``` 
