if exists("g:loaded_pandocViewer")
    finish
endif
let g:loaded_pandocViewer = 1

let s:save_cpo = &cpo
set cpo&vim

let g:pandocViewer_lineSaveToggle = 1
autocmd BufWrite *.{md} :call pandocViewer#SaveCurrentRow()
autocmd BufWrite *.{mediawiki} :call pandocViewer#SaveCurrentRow()

command! PandocPreview call pandocViewer#RunPandccPreview()

let &cpo = s:save_cpo
unlet s:save_cpo
