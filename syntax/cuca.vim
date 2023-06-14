" Vim syntax file
" Language:     Cuca
" Maintainer:   Otavio Pontes
" Filenames:    *.cuca

if exists("b:current_syntax")
  finish
endif

if !exists('main_syntax')
  let main_syntax = 'cuca'
endif


" Special hightlights

runtime! syntax/markdown.vim
unlet! b:current_syntax

syn region markdownWikiRef matchgroup=markdownWikiRefDelimiter start="\[" end="\]" skip="\] \?(" keepend oneline

hi def link markdownWikiRef               Type
hi def link markdownWikiRefDelimiter      Type

let b:current_syntax = "cuca"
if main_syntax ==# 'cuca'
  unlet main_syntax
endif
