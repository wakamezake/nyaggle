"""
Modified work:
-----------------------------------------------------------------------------
Copyright (c) 2020 Kota Yuhara (@wakamezake)
-----------------------------------------------------------------------------

Original work of aggregation:
https://github.com/pfnet-research/xfeat/blob/master/xfeat/helper.py
-----------------------------------------------------------------------------
MIT License

Copyright (c) 2020 Preferred Networks, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-----------------------------------------------------------------------------
"""

from typing import List, Callable, Union

import pandas as pd


def aggregation(
        input_df: pd.DataFrame,
        group_key: str,
        group_values: List[str],
        agg_methods: List[Union[str, Callable]],
):
    """Aggregate values after grouping table rows by a given key.
    Args:
        input_df:
            Input data frame.
        group_key:
            Used to determine the groups for the groupby.
        group_values:
            Used to aggregate values for the groupby.
        agg_methods:
            List of function or function names,
             e.g. ['mean', 'max', 'min', numpy.mean].
    Returns:
        Tuple of output dataframe and new column names.
    """
    new_df = input_df.copy()

    new_cols = []
    for agg_method in agg_methods:
        for col in group_values:
            if isinstance(agg_method, str):
                agg_method_name = agg_method
            elif isinstance(agg_method, Callable):
                agg_method_name = agg_method.__name__
            else:
                raise ValueError(f'Supported types are: {str} or {Callable}.'
                                 f' Got {type(agg_method)} instead.')
            new_col = f"agg_{agg_method_name}_{col}_by_{group_key}"

            df_agg = (
                input_df[[col] + [group_key]].groupby(group_key)[[col]].agg(
                    agg_method)
            )
            df_agg.columns = [new_col]
            new_cols.append(new_col)
            new_df = new_df.merge(
                df_agg, how="left", right_index=True, left_on=group_key
            )

    return new_df, new_cols