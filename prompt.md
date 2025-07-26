## Prompt POC phase
### Phase 1 prompt
```
${file_content}
according to above mkdocs.yml, 
- which i18n does the project cover? 
- what's the naming rule or file path rule for i18n mapping between different language edition?
```

```
here is the tree command result for docs folder
${tree list}
could you please list the missing file in support language? please result in mapping as source file, support file.
```

### Phase 2 prompt
```
please help translate content below into Chinese for me, please keep kepler in english and keep the markdown style, here is the content:

file_content
```

## Structure Prompt phase