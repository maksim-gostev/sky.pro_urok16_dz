
def instance_to_dict_users(instance):
    return {
        "age": instance.age,
        "email": instance.email,
        "first_name": instance.first_name,
        "id": instance.id,
        "last_name": instance.last_name,
        "phone": instance.phone,
        "role": instance.role,
    }
def instance_to_dict_offers(instance):
    return {
        "executor_id": instance.executor_id,
        "id": instance.id,
        "order_id": instance.order_id,
    }

def instance_to_dict_orders(instance):
    return {
        "address": instance.address,
        "customer_id": instance.customer_id,
        "description": instance.description,
        "end_date": instance.end_date,
        "executor_id": instance.executor_id,
        "id": instance.id,
        "name": instance.name,
        "price": instance.price,
        "start_date": instance.start_date
    }
