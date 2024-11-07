### Where Monolithic fails?
##### Scaling
Lets say we have an application where we have lots of different components like orders, payments and products (each are having different IDs) **tightly coupled** in one piece. Scaling it could be difficult - if the orders part is having more traffic, still we need to scale the entire application.

### Disadvantages of Microservices
##### Know where/how to break
You need to understand when to break a monolithic one into microservices - if there is tight coupling, then changing at one place requires change at a lot of places. And know how to break the application in a microservice architecture.

##### Hard to monitor which services are using the current service
If S3 is being deployed after updating, and assume that S2 is using S3 after changing, it can break, hence monitoring is difficult.

##### Transaction is difficult
Transaction management - each service is having different DB so a single transaction cannot be done, need some debugging to understand for which DB it got failed.

### Breaking monolithic into microservices is fine, but how small? 
There are various patterns to achieve this. To understand that, understand how all these fit in the whole architecture. All these are patterns (ways we can solve the breaking into microservices problem)

1. Decomposoition
    + How do you want to decompose the application? - Can do it by business capability, subdomain
    + For business capability/functionality, we can divide the ecommerce application into - login micro, billing micro, payment micro, products catalogue micro, etc.
    + For subdomain division, we are taking the whole functionality as the domain, and making microservices for each in that - "payment domain", "billing domain"
2. Database
    + Shared DB or different DB per service?
3. Communication
    + How are the different services communicating? - By API call or events,
4. Integration
    + How are all of these integrated in the whole architecture? Like with UI, etc.
