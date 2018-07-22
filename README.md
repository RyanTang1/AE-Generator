# Adversarial Image Generator

This project provides a pipeline from generating adversarial images from different attack methods to evaluate the accuracy from those methods. We use the implementation of [CleverHans](https://github.com/tensorflow/cleverhans#setting-up-cleverhans) library and use binary search to find the smallest peturbation that is needed to generate an adversarial example.

The code is currently used in the website [ADVex](https://advex.org), which is a website that helps users
to evaluate the robustness of their model. More details can be found there.

## Usage

The script is originally writtin based on taking the input data like imageNet validation data. Therefore, running the script requires several inputs.



### Model file

Typically saved using [keras save method](https://keras.io/getting-started/faq/#how-can-i-save-a-keras-model)

### Index to label mapping of your model

We provide a example in ```imagenet_class_index.json```. Unlike the origianl json file provided by the imagenet, our value should only be a string that represent the classID.

### Data

We use [ILSVRC](http://www.image-net.org/challenges/LSVRC/2012/index) validation data to generate the images.

Just like the how imagenet validation data is organized.
Images is named with index i.e ILSVRC2012_val_00025012.JPEG.
Here we assume the index 00025012 should be the last thing in the naming. Labels on the other hand, are stored in a text file with labels of every images starting from index 0.

Notice that if the index to label mapping of the data is different from the model, then you need to provide the mapping of index to label of the data as well. In our case, the mapping of the model is differnt from the data. So for example, 96 means toucan in the model but chimpanzee in the data.

### Config file

Config file provides parameter of the attack method. We provide an example in the ```config.py```

## Example

You can see other hyperparmeter using this command.

```bash
python prepare_adversarial_images.py -h
```


One example of running the script is shown below.

```bash
python prepare_adversarial_images.py --model ./vgg16.h5 --class_index ./imagenet_class_index.json --num_step 1 --num_generate 10 --data_input . --data_label ILSVRC2012_validation_ground_truth.txt --data_mapping ./class_index.json --config config.json --output_original --output_path ./image_final/
```

Our orginal setting is to use three attacks (FGSM,I-FGSM,MI-FGSM) to generate adversarial exampels.

## Evaluation

We provide a evaluation module in the ```evaluation``` script, you will have to provide your_model that is saved by keras's save function `model.save` ,a JSON file that contains a mapping between index to label and the path to where the adversarial images are stored.

To run the script. Use the following command

```bash
python evaluation.py --model YOUR_MODEL_PATH --index YOUR_INDEX_MAPPING --AE_path directory of your AE
```
