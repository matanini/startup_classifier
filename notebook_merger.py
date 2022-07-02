import nbformat

# Reading the notebooks
first_notebook = nbformat.read('1-data-scrape.ipynb', 4)
second_notebook = nbformat.read('2-data-cleaning.ipynb', 4)
third_notebook = nbformat.read('3-outlier-detection.ipynb', 4)
fourth_notebook = nbformat.read('4-eda-and-pca.ipynb', 4)
fith_notebook = nbformat.read('5-supervised.ipynb', 4)


# Creating a new notebook
final_notebook = nbformat.v4.new_notebook(metadata=first_notebook.metadata)

# Concatenating the notebooks
final_notebook.cells = first_notebook.cells + second_notebook.cells + third_notebook.cells + fourth_notebook.cells + fith_notebook.cells

# Saving the new notebook 
nbformat.write(final_notebook, 'final_notebook.ipynb')