# Automated Reports

## Coverage Report
```text
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
cli/__init__.py          0      0   100%
core/__init__.py         0      0   100%
pygame/__init__.py       0      0   100%
--------------------------------------------------
TOTAL                    0      0   100%

```

## Pylint Report
```text
************* Module computacion-2025-backgammon-carlastacchiola.core.checker
core/checker.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/checker.py:4:0: E0401: Unable to import 'core.board' (import-error)
core/checker.py:4:0: W0611: Unused BLACK imported from core.board (unused-import)
************* Module computacion-2025-backgammon-carlastacchiola.core.backgammon_game
core/backgammon_game.py:35:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon_game.py:197:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammon_game.py:211:0: C0301: Line too long (110/100) (line-too-long)
core/backgammon_game.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/backgammon_game.py:7:0: C0115: Missing class docstring (missing-class-docstring)
core/backgammon_game.py:20:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:24:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:24:4: C0104: Disallowed name "bar" (disallowed-name)
core/backgammon_game.py:28:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:39:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:42:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:45:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:113:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:113:4: R0911: Too many return statements (7/6) (too-many-return-statements)
core/backgammon_game.py:138:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:141:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:144:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:154:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:174:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:191:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:199:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:210:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:215:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:219:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:222:4: C0116: Missing function or method docstring (missing-function-docstring)
core/backgammon_game.py:7:0: R0904: Too many public methods (25/20) (too-many-public-methods)
************* Module computacion-2025-backgammon-carlastacchiola.core.board
core/board.py:213:0: C0304: Final newline missing (missing-final-newline)
core/board.py:1:0: C0114: Missing module docstring (missing-module-docstring)
core/board.py:18:8: C0104: Disallowed name "bar" (disallowed-name)
core/board.py:50:4: C0116: Missing function or method docstring (missing-function-docstring)
core/board.py:103:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
core/board.py:98:4: R0911: Too many return statements (9/6) (too-many-return-statements)
core/board.py:98:4: R0912: Too many branches (13/12) (too-many-branches)
core/board.py:160:4: R0911: Too many return statements (8/6) (too-many-return-statements)
************* Module computacion-2025-backgammon-carlastacchiola.core.player
core/player.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module computacion-2025-backgammon-carlastacchiola.core.dice
core/dice.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module computacion-2025-backgammon-carlastacchiola.cli.cli
cli/cli.py:28:0: C0301: Line too long (103/100) (line-too-long)
cli/cli.py:55:0: C0301: Line too long (108/100) (line-too-long)
cli/cli.py:63:0: C0301: Line too long (106/100) (line-too-long)
cli/cli.py:1:0: C0114: Missing module docstring (missing-module-docstring)
cli/cli.py:3:0: E0401: Unable to import 'core.backgammon_game' (import-error)
cli/cli.py:71:20: R1724: Unnecessary "else" after "continue", remove the "else" and de-indent the code inside it (no-else-continue)
************* Module computacion-2025-backgammon-carlastacchiola.pygame.pygame_ui
pygame/pygame_ui.py:105:0: C0301: Line too long (107/100) (line-too-long)
pygame/pygame_ui.py:116:0: C0301: Line too long (106/100) (line-too-long)
pygame/pygame_ui.py:119:0: C0301: Line too long (106/100) (line-too-long)
pygame/pygame_ui.py:128:0: C0301: Line too long (122/100) (line-too-long)
pygame/pygame_ui.py:132:0: C0301: Line too long (122/100) (line-too-long)
pygame/pygame_ui.py:175:0: C0301: Line too long (105/100) (line-too-long)
pygame/pygame_ui.py:189:0: C0301: Line too long (101/100) (line-too-long)
pygame/pygame_ui.py:194:0: C0301: Line too long (103/100) (line-too-long)
pygame/pygame_ui.py:202:0: C0301: Line too long (103/100) (line-too-long)
pygame/pygame_ui.py:203:0: C0301: Line too long (111/100) (line-too-long)
pygame/pygame_ui.py:239:0: C0301: Line too long (115/100) (line-too-long)
pygame/pygame_ui.py:239:0: W0311: Bad indentation. Found 28 spaces, expected 24 (bad-indentation)
pygame/pygame_ui.py:240:0: W0311: Bad indentation. Found 32 spaces, expected 28 (bad-indentation)
pygame/pygame_ui.py:241:0: W0311: Bad indentation. Found 32 spaces, expected 28 (bad-indentation)
pygame/pygame_ui.py:242:0: W0311: Bad indentation. Found 28 spaces, expected 24 (bad-indentation)
pygame/pygame_ui.py:243:0: W0311: Bad indentation. Found 32 spaces, expected 28 (bad-indentation)
pygame/pygame_ui.py:244:0: W0311: Bad indentation. Found 28 spaces, expected 24 (bad-indentation)
pygame/pygame_ui.py:247:0: C0301: Line too long (115/100) (line-too-long)
pygame/pygame_ui.py:247:0: W0311: Bad indentation. Found 28 spaces, expected 24 (bad-indentation)
pygame/pygame_ui.py:248:0: W0311: Bad indentation. Found 32 spaces, expected 28 (bad-indentation)
pygame/pygame_ui.py:249:0: W0311: Bad indentation. Found 32 spaces, expected 28 (bad-indentation)
pygame/pygame_ui.py:250:0: W0311: Bad indentation. Found 28 spaces, expected 24 (bad-indentation)
pygame/pygame_ui.py:251:0: W0311: Bad indentation. Found 32 spaces, expected 28 (bad-indentation)
pygame/pygame_ui.py:252:0: W0311: Bad indentation. Found 28 spaces, expected 24 (bad-indentation)
pygame/pygame_ui.py:260:0: C0301: Line too long (107/100) (line-too-long)
pygame/pygame_ui.py:289:0: C0301: Line too long (116/100) (line-too-long)
pygame/pygame_ui.py:295:0: C0301: Line too long (111/100) (line-too-long)
pygame/pygame_ui.py:321:0: C0301: Line too long (116/100) (line-too-long)
pygame/pygame_ui.py:323:0: C0301: Line too long (118/100) (line-too-long)
pygame/pygame_ui.py:329:0: C0301: Line too long (105/100) (line-too-long)
pygame/pygame_ui.py:1:0: C0114: Missing module docstring (missing-module-docstring)
pygame/pygame_ui.py:4:0: E0401: Unable to import 'core.backgammon_game' (import-error)
pygame/pygame_ui.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
pygame/pygame_ui.py:30:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
pygame/pygame_ui.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)
pygame/pygame_ui.py:38:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
pygame/pygame_ui.py:46:0: C0116: Missing function or method docstring (missing-function-docstring)
pygame/pygame_ui.py:54:0: C0116: Missing function or method docstring (missing-function-docstring)
pygame/pygame_ui.py:72:0: C0116: Missing function or method docstring (missing-function-docstring)
pygame/pygame_ui.py:77:0: C0115: Missing class docstring (missing-class-docstring)
pygame/pygame_ui.py:77:0: R0902: Too many instance attributes (9/7) (too-many-instance-attributes)
pygame/pygame_ui.py:79:8: E1101: Module 'pygame' has no 'init' member (no-member)
pygame/pygame_ui.py:99:4: C0116: Missing function or method docstring (missing-function-docstring)
pygame/pygame_ui.py:99:4: R0914: Too many local variables (23/15) (too-many-locals)
pygame/pygame_ui.py:122:50: E1101: Module 'pygame' has no 'SRCALPHA' member (no-member)
pygame/pygame_ui.py:99:25: W0613: Unused argument 'legal_from' (unused-argument)
pygame/pygame_ui.py:181:4: C0116: Missing function or method docstring (missing-function-docstring)
pygame/pygame_ui.py:196:35: W0212: Access to a protected member _point_is_blocked of a client class (protected-access)
pygame/pygame_ui.py:183:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
pygame/pygame_ui.py:202:31: W0212: Access to a protected member _dest_index of a client class (protected-access)
pygame/pygame_ui.py:203:51: W0212: Access to a protected member _point_is_blocked of a client class (protected-access)
pygame/pygame_ui.py:218:33: E1101: Module 'pygame' has no 'QUIT' member (no-member)
pygame/pygame_ui.py:221:35: E1101: Module 'pygame' has no 'KEYDOWN' member (no-member)
pygame/pygame_ui.py:221:67: E1101: Module 'pygame' has no 'K_SPACE' member (no-member)
pygame/pygame_ui.py:227:35: E1101: Module 'pygame' has no 'MOUSEBUTTONDOWN' member (no-member)
pygame/pygame_ui.py:183:8: R1702: Too many nested blocks (7/5) (too-many-nested-blocks)
pygame/pygame_ui.py:183:8: R1702: Too many nested blocks (7/5) (too-many-nested-blocks)
pygame/pygame_ui.py:295:39: W0212: Access to a protected member _dest_index of a client class (protected-access)
pygame/pygame_ui.py:183:8: R1702: Too many nested blocks (7/5) (too-many-nested-blocks)
pygame/pygame_ui.py:326:36: R1724: Unnecessary "else" after "continue", remove the "else" and de-indent the code inside it (no-else-continue)
pygame/pygame_ui.py:351:8: E1101: Module 'pygame' has no 'quit' member (no-member)
pygame/pygame_ui.py:181:4: R0912: Too many branches (51/12) (too-many-branches)
pygame/pygame_ui.py:181:4: R0915: Too many statements (115/50) (too-many-statements)
pygame/pygame_ui.py:183:8: R1702: Too many nested blocks (9/5) (too-many-nested-blocks)

-----------------------------------
Your code has been rated at 7.80/10


```
