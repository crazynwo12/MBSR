#


#python main.py --model EDSR --scale 2 --save EDSR_difficult_Final_x2_1_0320_retrain_update --reset --chop_forward   --pre_train_1 ../experiment/EDSR_difficult_Final_x2_1_0320_retrain/model/model_34.pt
#--pre_train_1 ../experiment/EDSR_bicubic_Final_x2_1_0315/model/model_50.pt  #--pre_train_2 ../experiment/EDSR_baseline_x4_2/model/model_268.pt --pre_train_3 ../experiment/EDSR_bicubic_baseline_x8_4_0315_2/model/model_26.pt

#
#
# Test your own images
python main.py --scale 2 --data_test MyImage --test_only --save_results --pre_train_1 ../experiment/EDSR_difficult_Final_x2_1_0320_retrain_update/model/model_2.pt  --self_ensemble





#Advanced - JPEG artifact removal
#python main.py --template MDSR_jpeg --model MDSR --scale 2+3+4 --save MDSR_jpeg --quality 75+ --reset
