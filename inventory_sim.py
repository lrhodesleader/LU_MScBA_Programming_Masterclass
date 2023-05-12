from numpy.random import default_rng

# time horizon in days
horizon = 10
# mean daily demand
mean_demand = 50
# selling price of the product
price = 10
# cost of buying the product
unit_cost = 5
# delivery cost
fixed_cost = 10
# cost per day of storage
storage_cost = 2
# cost of a stockout
stockout_cost = 50

def inventory_simulation(capacity,reorder_level,reps,seed=None):
    """
    Simulation model for a (S,s) inventory system. 
    - Demand comes from a Poisson distribution, and is generated each day
    - If possible, all demand is satisfied that day.
    - Once the inventory has gone below s = reorder_level, an order is placed 
        to restock up to S = capacity, which happens over night.
    - costs include stockout cost, item order cost, fixed order cost and a 
        holding cost

    Parameters
    ----------
    capacity : int
        Maximum capacity.
    reorder_level : int
        Level below which the .
    reps : int
        Number of times to simulate the time horizon.
    seed : int, optional
        Seed for the random number generator. The default is None.

    Returns
    -------
    A list of the profits over the time horizon for each replication.

    """
    output = []
    # initiate the random number generator.
    rng = default_rng(seed)
    
    # loop over the replications
    for r in range(reps):
        
        inventory = capacity
        profit = 0
        
        # iterate over the time period
        for day in range(horizon):
            # generate demand
            demand = rng.poisson(mean_demand)
            # calculate revenue
            revenue = min(inventory, demand)*price
            
            # stockout?
            stockout = 1 if demand > inventory else 0
            
            # update the inventory
            inventory = min(inventory - demand, 0)
            
            # are any orders needed
            if inventory <= reorder_level:
                order_size = capacity - inventory
                order_cost = fixed_cost + order_size*unit_cost
                
            else:
                order_cost = 0
            
            # holding cost
            holding_cost = storage_cost*inventory
            
            # update profit
            profit += revenue - order_cost - holding_cost - stockout*stockout_cost
            
        output.append(profit)
    
    return(output)
                
                
x = inventory_simulation(100, 10, 1, 1)
print(x)

