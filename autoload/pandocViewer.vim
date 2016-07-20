let s:save_cpo = &cpo
set cpo&vim

let s:this_dir = expand("<sfile>:h")
let s:pyscript_dir = s:this_dir . "/pandocViewer.py"
let s:pyscript = substitute(s:pyscript_dir, "\\", "/", "g")
let s:default_css = s:this_dir . "/github.css"

function! pandocViewer#RunPandccPreview() abort
    let l:current_file = expand("%:p")

    if has('win32') || has('win64')
        silent exe
            \"!start python " .
            \shellescape(s:pyscript) .
            \" " . shellescape(l:current_file) .
            \" " . shellescape(g:pandocViewer_css_path)
    else
        call system(
            \"python " .
            \s:pyscript .
            \" " . l:current_file .
            \" " . g:pandocViewer_css_path . " &")
    endif
endfunction

function! pandocViewer#SaveCurrentRow() abort
    if g:pandocViewer_lineSaveToggle == 1
        let l:bottomLine = line("$")
        let l:topLine = 1.0
        let l:currentLine = (line("."))
        let l:percentage = round(
            \l:currentLine * l:topLine / l:bottomLine * 100)
        
        let l:lineInfoFile_temp = 
            \s:this_dir . "/pandocViewer_lineInfo.txt"
        let l:lineInfoFile = substitute(
            \l:lineInfoFile_temp, "\\", "/", "g")
        
        execute ":redir! > " .l:lineInfoFile 
        silent! echon float2nr(l:percentage) . "\n"
        redir END
    endif
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
