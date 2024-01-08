import random

def get_WIDTH_HEIGHT():
    WIDTH = 1074
    HEIGHT = 654
    return WIDTH, HEIGHT

def researches_get_list(research_result):
    global research_days, research_started, MONEY, SKILLS
    if research_result == 1:
        return ['усиление бонуса ремонта на', random.choice([0.2, 0.1, 0.05, 0.01])]
    elif research_result == 2:
        return ['усиление продажи без ремонта на', random.choice([0.02, 0.1, 0.05, 0.01])]
    elif research_result == 3:
        return ['усиление бонуса получения ОН на', random.choice([1, 2, 3])]
    elif research_result == 4:
        return ['очки навыка', random.randint(1, 20)]
    elif research_result == 5:
        return ['деньги', random.randint(5000, 50000)]

def get_colors():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREY = (80, 80, 80)
    GREY_GAME = (44, 47, 54)
    return [WHITE, BLACK, RED, GREEN, BLUE, YELLOW, GREY, GREY_GAME]

def get_data_for_new_game():
    can_buy = True
    is_repaired = False
    old_repair_cost_PC = 0

    MONEY = 20000
    DAY = 0
    SKILLS = 0
    
    SKILL_BONUS = 1
    warehouse_log = ''
    repair_bonus = 0
    bonus_sales = 0
    
    DEBT = 100000
    stocks_cost = random.randint(11000, 25000)
    stocks_list = [stocks_cost]
    stocks = False
    spent_per_turn = 0
    received_per_turn = 0
    day_get_crdit = 10
    company = False
    company_profit = 0
    
    total_sold = 0
    total_money_spent = 0
    total_money_earned = 0
    purchased_for = None

    research_started = False
    research_days = 0
    research_result = researches_get_list(random.randint(1, 5))

    mind = 100

    company_profit_upgrade_cost_now = 50
    company_profit_upgrade_levl_now = 0

    SKILL_BONUS_upgrade_cost_now = 3
    SKILL_BONUS_upgrade_levl_now = 0

    repair_bonus_upgrade_cost_now = 3
    repair_bonus_upgrade_levl_now = 0

    bonus_sales_upgrade_cost_now = 3
    bonus_sales_upgrade_levl_now = 0

    return [can_buy, is_repaired, old_repair_cost_PC, MONEY,
            DAY, SKILLS, SKILL_BONUS, warehouse_log, repair_bonus,
            bonus_sales, DEBT, stocks_cost, stocks_list, stocks,
            spent_per_turn, received_per_turn, day_get_crdit, company, company_profit,
            total_sold, total_money_spent, total_money_earned, purchased_for,
            research_started, research_days, research_result,
            company_profit_upgrade_cost_now, company_profit_upgrade_levl_now,
            SKILL_BONUS_upgrade_cost_now, SKILL_BONUS_upgrade_levl_now,
            repair_bonus_upgrade_cost_now, repair_bonus_upgrade_levl_now,
            bonus_sales_upgrade_cost_now, bonus_sales_upgrade_levl_now, mind]
            
