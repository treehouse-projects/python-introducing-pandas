from IPython.display import display, Markdown

def render(md):
    return display(Markdown(md))

def make_chaos(df, sample_size, columns, fn):
    # Keep chaos the same randomly
    some = df.sample(sample_size, random_state=sample_size)
    for col in columns:
        some[col] = some[col].apply(fn)
    # Update the original DataFrame
    df.update(some)