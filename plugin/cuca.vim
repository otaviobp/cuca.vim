if !has('python3')
    echomsg 'python3 support needed to run cuca.vim'
    finish
endif

python3 import cuca_vim

command! -nargs=1 CucaAddURL python3 cuca_vim.CucaAddURL(<f-args>)
command! -nargs=1 CucaAddFile python3 cuca_vim.CucaAddFile(<f-args>)
command! CucaOpen python3 cuca_vim.CucaOpen()
command! CucaBack python3 cuca_vim.CucaBack()
command! CucaFix python3 cuca_vim.CucaFix()
command! CucaCreateHTML python3 cuca_vim.CucaCreateHTML()
command! CucaOpenInBrowser python3 cuca_vim.CucaOpenInBrowser()

" au BufNewFile,BufRead *.cuca  setf cuca
augroup CucaShortcut
    " <C-j>: Look for note and add a link
    " autocmd FileType markdown inoremap <buffer> <C-j> <C-o>:call fzf#run({'sink': 'notesHandleFZF'})<CR>

    " <enter>: Open selected entry and create if not exists
    autocmd FileType cuca nnoremap <buffer> <enter> :CucaOpen<CR>

    " <C-S>: Add url
    autocmd FileType cuca inoremap <buffer> <C-S> <Esc>:CucaAddURL 

    " <C-I>: Add Img
    autocmd FileType cuca inoremap <buffer> <C-F> <Esc>:CucaAddFile 

    " <C-X>: Go back to file on stack
    autocmd FileType cuca nnoremap <buffer> <C-X> :CucaBack<CR>

    " <C-F>: Open note on browser
    autocmd FileType cuca nnoremap <buffer> <C-B> :CucaOpenInBrowser<CR>

    " Generate HTML on save
    autocmd BufWritePost *.cuca :CucaFix
    autocmd BufWritePost *.cuca :CucaCreateHTML
augroup END

