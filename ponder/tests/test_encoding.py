
'''Test encode() directly'''

# TODO: loop over some datasets
#  include datasets with grouped column levels

import pytest

from io import StringIO
#import numpy as np

from .utils import parse_test_df
from ..ponder import encode

random1 = """
Boolean,Float,Integer,Binary,Ordinal,Nominal,Nominal2
False,-91.70353154100944,-19,No,Small,Yellow,PositiveA
False,-100.7646044339111,-29,Yes,Large,Yellow,PositiveA
False,-47.31856770249317,-35,No,Medium,Green,PositiveA
False,-73.25058305886796,-36,Yes,Small,Red,PositiveA
True,-73.3503264846611,-20,No,Medium,Green,PositiveA
False,-64.410365287374,38,Yes,Medium,Green,Negative
True,-56.42366099770481,83,No,Large,Yellow,PositiveB
False,-90.07982302278825,40,Yes,Medium,Red,Negative
True,-85.87752953888797,-16,No,Small,Yellow,Negative
True,-72.7651790369317,77,No,Medium,Red,PositiveA
False,-72.58103656260525,33,No,Large,Green,PositiveB
True,-67.39009596421542,54,Yes,Large,Yellow,PositiveB
False,-50.69539480986763,-22,No,Medium,Yellow,PositiveA
False,-79.38723920885045,53,No,Small,Red,PositiveA
False,-75.319654916638,66,Yes,Small,Green,PositiveA
False,-86.78651562886694,53,Yes,Small,Red,PositiveB
False,-71.94628003068131,34,Yes,Small,Green,Negative
False,-102.62798417179903,65,No,Medium,Yellow,Negative
False,-67.68842323268751,58,No,Medium,Yellow,Negative
False,-74.1392350947031,-27,No,Large,Yellow,PositiveB
True,-98.23995635089136,36,No,Small,Green,PositiveA
False,-69.99687745910832,-10,No,Small,Red,PositiveA
False,-106.43248137769748,4,No,Small,Red,PositiveB
False,-118.60379759970355,60,No,Small,Green,Negative
True,-52.28409062737161,43,Yes,Large,Red,PositiveB
False,-29.69941718494491,-14,No,Medium,Green,Negative
False,-99.31554758322726,36,No,Small,Yellow,PositiveA
True,-89.3972793730313,-16,Yes,Medium,Yellow,PositiveA
False,-100.50202025661773,-33,No,Small,Green,PositiveA
False,-82.6927322447452,50,No,Small,Green,PositiveA
"""

random1_basic_columns = ['Boolean_False', 'Boolean_True',
    'Binary_No', 'Binary_Yes',
    'Ordinal_Small', 'Ordinal_Medium',
    'Ordinal_Large', 'Nominal_Red', 'Nominal_Yellow', 'Nominal_Green',
    'Nominal_Purple', 'Nominal2_Negative', 'Nominal2_PositiveA',
    'Nominal2_PositiveB', 'Float', 'Integer']

random1_basic_mapping = {
    'Boolean': [False, True], 'Binary': ['No', 'Yes'],
    'Ordinal': ['Small', 'Medium', 'Large'],
    'Nominal': ['Red', 'Yellow', 'Green', 'Purple'],
    'Nominal2': ['Negative', 'PositiveA', 'PositiveB']}

random1_basic_bases = {
    'Boolean': None, 'Binary': None, 'Ordinal': None,
    'Nominal': None, 'Nominal2': None}

random1_noexpand_columns = [
    'Boolean_True', 'Binary_Yes',
    'Ordinal_Small', 'Ordinal_Medium',
    'Ordinal_Large', 'Nominal_Red', 'Nominal_Yellow', 'Nominal_Green',
    'Nominal_Purple', 'Nominal2_Negative', 'Nominal2_PositiveA',
    'Nominal2_PositiveB', 'Float', 'Integer']

random1_noexpand_mapping = random1_basic_mapping

random1_noexpand_bases = {
    'Boolean': False, 'Binary': 'No', 'Ordinal': None,
    'Nominal': None, 'Nominal2': None}

random1_basecats_columns = [
    'Boolean_True', 'Binary_Yes',
    'Ordinal_Small', 'Ordinal_Medium',
    'Ordinal_Large', 'Nominal_Red', 'Nominal_Yellow', 'Nominal_Green',
    'Nominal_Purple', 'Nominal2_PositiveA',
    'Nominal2_PositiveB', 'Float', 'Integer']

random1_basecats_mapping = random1_basic_mapping

random1_basecats_bases = {
    'Boolean': False, 'Binary': 'No', 'Ordinal': None,
    'Nominal': None, 'Nominal2': 'Negative'}


# Test sets and tests

basics_tests = [
    (random1, random1_basic_columns, random1_basic_mapping,
    random1_basic_bases)]

@pytest.mark.parametrize("df_str,exp_columns,exp_mapping,exp_bases",
        basics_tests)
def test_encode_basics(df_str, exp_columns, exp_mapping, exp_bases):
    '''
    Test encode with the simplest possible settings:
    all fields as columns (so expand_binary=True and no base categories),
    no grouped columns.
    '''
    df = parse_test_df(StringIO(df_str))
    # add an unobserved category to one variable
    df['Nominal'].cat.set_categories(['Red', 'Yellow', 'Green', 'Purple'],
                                 inplace=True)
    encoded, mapping, bases = encode(df, expand_binary=True)
    assert set(encoded.columns)==set(exp_columns)
    assert mapping==exp_mapping
    assert bases==exp_bases


noexpand_tests = [
    (random1, random1_noexpand_columns, random1_noexpand_mapping,
    random1_noexpand_bases)]

@pytest.mark.parametrize("df_str,exp_columns,exp_mapping,exp_bases",
        noexpand_tests)
def test_encode_noexpand(df_str, exp_columns, exp_mapping, exp_bases):
    '''
    Test encode with expand_binary=False (the default).
    '''
    df = parse_test_df(StringIO(df_str))
    # add an unobserved category to one variable
    df['Nominal'].cat.set_categories(['Red', 'Yellow', 'Green', 'Purple'],
                                      inplace=True)
    encoded, mapping, bases = encode(df, expand_binary=False)
    assert set(encoded.columns)==set(exp_columns)
    assert mapping==exp_mapping
    assert bases==exp_bases


basecategories_tests = [
    (random1, random1_basecats_columns, random1_basecats_mapping,
    random1_basecats_bases)]

@pytest.mark.parametrize("df_str,exp_columns,exp_mapping,exp_bases",
        basecategories_tests)
def test_encode_basecategories(df_str, exp_columns, exp_mapping, exp_bases):
    '''
    Test encode with base categories, and default expand_binary=False.
    '''
    df = parse_test_df(StringIO(df_str))
    # add an unobserved category to one variable
    df['Nominal'].cat.set_categories(['Red', 'Yellow', 'Green', 'Purple'],
                                      inplace=True)
    # set Nominal2 base, and add an irrelevant, unused base
    encoded, mapping, bases = encode(df,
                        base_categories={'Nominal2':'Negative',
                                         'Irrelevant':'Neg'})
    assert set(encoded.columns)==set(exp_columns)
    assert mapping==exp_mapping
    assert bases==exp_bases
