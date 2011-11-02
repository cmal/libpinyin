# -*- coding: utf-8 -*-
# vim:set et sts=4 sw=4:
#
# libpinyin - Library to deal with pinyin.
#
# Copyright (C) 2011 Peng Wu <alexepico@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import operator
from pinyintable import *


content_table = []
pinyin_index = []
bopomofo_index = []

#pinyin table
def filter_pinyin_list():
    for (correct, wrong, bopomofo, flags, chewing) in gen_pinyin_list():
        flags = '|'.join(flags)
        chewing = "ChewingKey({0})".format(', '.join(chewing))
        content_table.append((correct, bopomofo, chewing))
        if "IS_PINYIN" in flags:
            pinyin_index.append((wrong, flags, correct))
        if "IS_CHEWING" in flags:
            bopomofo_index.append((bopomofo, flags, bopomofo))


def sort_all():
    global content_table, pinyin_index, bopomofo_index
    #remove duplicates
    content_table = list(set(content_table))
    #define sort function
    sortfunc = operator.itemgetter(0)
    #begin sort
    content_table = sorted(content_table, key=sortfunc)
    #prepend zero item
    content_table.insert(0, ("", "", "ChewingKey()"))
    #sort index
    pinyin_index = sorted(pinyin_index, key=sortfunc)
    bopomofo_index = sorted(bopomofo_index, key=sortfunc)


def gen_context_table():
    entries = []
    for ((correct, bopomofo, chewing)) in content_table:
        entry = '{{"{0}", "{1}", {2}}}'.format(correct, bopomofo, chewing)
        entries.append(entry)
    return ',\n'.join(entries)


def gen_pinyin_index():
    entries = []
    for (wrong, flags, correct) in pinyin_index:
        index = [x[0] for x in content_table].index(correct)
        entry = '{{"{0}", {1}, {2}}}'.format(wrong, flags, index)
        entries.append(entry)
    return ',\n'.join(entries)


def gen_bopomofo_index():
    entries = []
    for (bopomofo_str, flags, bopomofo) in bopomofo_index:
        index = [x[0] for x in content_table].index(bopomofo)
        entry = '{{"{0}", {1}, {2}}}'.format(bopomofo_str, flags, index)
        entries.append(entry)
    return ',\n'.join(entries)


### main function ###
if __name__ == "__main__":
    filter_pinyin_list()
    sort_all()
    s = gen_pinyin_index()
    print(s)
