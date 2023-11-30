from src.deepReplication.dataPreperation.dataCombining import combine_data
from src.deepReplication.dataPreperation.scaling import scaling

def do_all_stuffs():
    combine_data(base_name='deepBollinger', identifier='test1bollinger', num_prev_prices=20, drop_nans=True)
    combine_data(base_name='deepTurtle', strategy='turtle_naive', identifier='test1turtles',
                 num_prev_prices=20, drop_nans=True)

    combine_data(base_name='deepBox', strategy='box_naive', identifier='test1box', num_prev_prices=20, drop_nans=True)