def calculate_days_calories(plan):
    """
    Calculate days calories amount for selected Plan model object.
    :param plan: Plan model object.
    :return: List of calories amount for every plan_day
    """
    days_calories_list = []
    for day in range(1, plan.plan_length + 1):
        day_meals = plan.meal_set.filter(plan_day=day)
        day_calories = 0
        for meal in day_meals:
            day_calories += float(meal.meal_portions) * float(meal.recipes.portion_calories)
        days_calories_list.append(round(day_calories, 2))
    return days_calories_list
