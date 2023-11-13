#! /usr/bin/env bash

jupyter nbconvert --to html --TagRemovePreprocessor.remove_input_tags 'hide-input' "project-6.ipynb"