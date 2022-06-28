from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

def vectorize_and_replace(df, cols: list, prefix: str):
    """Vectorize the {cols} columns in {dataframe}\n
    and returns a {dataframe} copy with the vector after removing the {cols}\n
    new col name is {prefix}_vec """
    # df = dataframe.copy()

    lb = preprocessing.LabelBinarizer()
    vec = lb.fit_transform(df[cols]).tolist()

    # vec = [int(x) for x in vec.split(',')]


    df[f"{prefix}_vec"] = vec
    df = df.drop(cols, axis = 1)
    return df


def decode_price(price: str):
    '''
    format: $XXXX.XXXXA 
    where X is digit from the range [0,9]
    and A is an action multiplier where K means thousands and M means Millions. 
    '''

    if(price[0]!='$'):
        price = '$' + price

    k = 1000
    m = 1000000
    multiplier = 0
    try:
        symbol = price[-1].upper() # The upper method is used to reduce the need to check wether the symbol is 'k' or 'K'
    except:
        print(f"Error: The end of the string '{price}' does not contain 'K' or 'M'!")
        return None
    if(symbol=="K"):
        multiplier = k
    elif(symbol == "M"):
        multiplier = m
    elif symbol == "B" :
        multiplier = m * 100
    else:
        return float(price[1:])
    
    new_price= int(float(price[1:-1]) * multiplier)
    # print(f"Price before manipulation: {price}")
    # print(f"Price after manipulation: {new_price}")

    # TODO: after the function test we can remove the prints above.
    
    return new_price

def conv_to_float(df):
    if df.dtype.kind not in "biufc":
        for i, val in enumerate(df):
            if val != 0:
                df.iloc[i] = decode_price(val)
                # print(f"{val} converted to {df.iloc[i]}")
    return df