from src.deepReplication.dataPreperation.dataCombining import combine_data
from src.deepReplication.dataPreperation.scaling import scaling

def do_all_stuffs():
    num_prev_prices = 20
    split_to_do = "34_33_33"

    combine_data(base_name='deepBollinger', strategy='bollinger_naive_dynamic_sl', identifier='test11bollinger', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)
    combine_data(base_name='deepBollinger', strategy='bollinger_naive_dynamic_sl', identifier='test22bollinger', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)
    combine_data(base_name='deepTurtle', strategy='turtle_naive', identifier='test1turtles', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)
    combine_data(base_name='deepBox', strategy='box_naive', identifier='test1box', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)

    scaling(base_name='Bollinger', identifier='test11bollinger', num_prev_price=num_prev_prices, splits=split_to_do)
    scaling(base_name='Bollinger', identifier='test22bollinger', num_prev_price=num_prev_prices, splits=split_to_do)
    scaling(base_name='Turtle', identifier='test1turtles', num_prev_price=num_prev_prices, splits=split_to_do)
    scaling(base_name='Box', identifier='test1box', num_prev_price=num_prev_prices, splits=split_to_do)


    split_to_do = "80_10_10"

    combine_data(base_name='deepBollinger', strategy='bollinger_naive_dynamic_sl', identifier='test11bollinger', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)
    combine_data(base_name='deepBollinger', strategy='bollinger_naive_dynamic_sl', identifier='test22bollinger', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)
    combine_data(base_name='deepTurtle', strategy='turtle_naive', identifier='test1turtles', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)
    combine_data(base_name='deepBox', strategy='box_naive', identifier='test1box', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)

    scaling(base_name='Bollinger', identifier='test11bollinger', num_prev_price=num_prev_prices, splits=split_to_do)
    scaling(base_name='Bollinger', identifier='test22bollinger', num_prev_price=num_prev_prices, splits=split_to_do)
    scaling(base_name='Turtle', identifier='test1turtles', num_prev_price=num_prev_prices, splits=split_to_do)
    scaling(base_name='Box', identifier='test1box', num_prev_price=num_prev_prices, splits=split_to_do)

    split_to_do = "10_80_10"

    combine_data(base_name='deepBollinger', strategy='bollinger_naive_dynamic_sl', identifier='test11bollinger', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)
    combine_data(base_name='deepBollinger', strategy='bollinger_naive_dynamic_sl', identifier='test22bollinger', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)
    combine_data(base_name='deepTurtle', strategy='turtle_naive', identifier='test1turtles', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)
    combine_data(base_name='deepBox', strategy='box_naive', identifier='test1box', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)

    scaling(base_name='Bollinger', identifier='test11bollinger', num_prev_price=num_prev_prices, splits=split_to_do)
    scaling(base_name='Bollinger', identifier='test22bollinger', num_prev_price=num_prev_prices, splits=split_to_do)
    scaling(base_name='Turtle', identifier='test1turtles', num_prev_price=num_prev_prices, splits=split_to_do)
    scaling(base_name='Box', identifier='test1box', num_prev_price=num_prev_prices, splits=split_to_do)

    split_to_do = "10_10_80"

    combine_data(base_name='deepBollinger', strategy='bollinger_naive_dynamic_sl', identifier='test11bollinger', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)
    combine_data(base_name='deepBollinger', strategy='bollinger_naive_dynamic_sl', identifier='test22bollinger', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)
    combine_data(base_name='deepTurtle', strategy='turtle_naive', identifier='test1turtles', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)
    combine_data(base_name='deepBox', strategy='box_naive', identifier='test1box', num_prev_prices=num_prev_prices, drop_nans=True, splits=split_to_do)

    scaling(base_name='Bollinger', identifier='test11bollinger', num_prev_price=num_prev_prices, splits=split_to_do)
    scaling(base_name='Bollinger', identifier='test22bollinger', num_prev_price=num_prev_prices, splits=split_to_do)
    scaling(base_name='Turtle', identifier='test1turtles', num_prev_price=num_prev_prices, splits=split_to_do)
    scaling(base_name='Box', identifier='test1box', num_prev_price=num_prev_prices, splits=split_to_do)