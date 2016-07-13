let s:this_dir = expand("<sfile>:h")

let s:pyscript_dir = s:this_dir . "/pandocViewer.py"
let s:pyscript = substitute(s:pyscript_dir, "\\", "/", "g")


function! RunPandccPreview() abort
    let l:current_file = "%:p"
    python import sys
    python sys.argv = ("arg1")
    if has('win32') || has('win64')
        silent exe "!start python " . shellescape(s:pyscript) . " " . shellescape(l:current_file)
    else
        echo ""
    endif
endfunction


function! SaveCurrentRow() abort
    if g:pandocViewer_lineSaveToggle == 1
        let l:bottomLine = line("$")
        let l:topLine = 1.0
        let l:currentLine = (line("."))
        let l:percentage = round(l:currentLine * l:topLine / l:bottomLine * 100)
        
        let l:lineInfoFile_temp = s:this_dir . "/pandocViewer_lineInfo.txt"
        let l:lineInfoFile = substitute(l:lineInfoFile_temp, "\\", "/", "g")
        
        execute ":redir! > " .l:lineInfoFile 
        silent! echon float2nr(l:percentage) . "\n"
        redir END
    endif
endfunction


let g:pandocViewer_lineSaveToggle = 1
autocmd BufWrite *.{md} :call SaveCurrentRow()
autocmd BufWrite *.{mediawiki} :call SaveCurrentRow()

command! PandocPreview call RunPandccPreview()
