"""Node Definitions

Defines all Nodes of the Brah Abstract Syntax Tree.
"""
from typing import Optional, Any, Union, List, Dict, Type
from brah.f_utils import DeclOffset


__all__ = [
    # functions
    'print_tree',

    # classes
    'ASTNode',
    'AddBinaryExprNode',
    'AggregateExprNode',
    'AliasTypeNode',
    'AndBinaryExprNode',
    'ArrayTypeNode',
    'AsmbNode',
    'AssignmentStmtNode',

    'BasicScopeNode',
    'BinaryExprNode',
    'BreakStmtNode',

    'CaseScopeNode',
    'CaseStmtNode',
    'ClassNameExprNode',
    'ClassTyclNode',
    'CompareBinaryExprNode',
    'ConstDeclNode',
    'ConstNameExprNode',
    'ContinueStmtNode',

    'DeclNode',
    'DecrUnaryExprNode',
    'DereferenceUnaryExprNode',
    'DirectCallExprNode',
    'DoUntilStmtNode',
    'DoWhileStmtNode',

    'EnumDeclNode',
    'EnumNameExprNode',
    'EnumTypeNode',
    'ExceptClauseStmtNode',
    'ExceptionNameExprNode',
    'ExceptionTypeNode',
    'ExprNode',
    'ExpressionStmtNode',

    'FieldDeclNode',
    'FieldNameExprNode',
    'FloatTypeNode',
    'ForEachStmtNode',
    'ForStmtNode',
    'FunctionDeclNode',
    'FunctionNameExprNode',
    'FunctionScopeNode',

    'GetterStmtNode',

    'IfElseStmtNode',
    'IfThenStmtNode',
    'ImportStmtNode',
    'IncrUnaryExprNode',
    'IndexExprNode',
    'IndirectCallExprNode',
    'IntegerTypeNode',
    'InterfaceTyclNode',

    'LValueExprNode',
    'LiteralExprNode',
    'LoopScopeNode',

    'MemberExprNode',
    'MethodDeclNode',
    'MethodScopeNode',
    'ModuleNode',
    'ModuleScopeNode',
    'MultBinaryExprNode',

    'NameExprNode',
    'NegateUnaryExprNode',

    'OrBinaryExprNode',

    'ParamDeclNode',
    'ParamNameExprNode',
    'PointerTypeNode',
    'PrimitiveTypeNode',
    'PropertyDeclNode',
    'PropertyNameExprNode',
    'PropertyScopeNode',

    'RaiseStmtNode',
    'ReferenceUnaryExprNode',
    'RepeatStmtNode',
    'ReturnStmtNode',

    'ScopeNode',
    'SetterStmtNode',
    'SignatureTypeNode',
    'SingletonTyclNode',
    'SourceNode',
    'StmtNode',
    'StringTypeNode',
    'StructNameExprNode',
    'StructureTyclNode',
    'SwitchStmtNode',

    'TemplNode',
    'TernaryExprNode',
    'TryScopeNode',
    'TryStmtNode',
    'TyclNode',
    'TypeNode',

    'UnaryExprNode',
    'UnpackStmtNode',
    'UnpackUnaryExprNode',

    'VarDeclNode',
    'VarNameExprNode',

    'WhileStmtNode',
]

# ---------------------------------------------------------
# region CONSTANTS & ENUMS

# endregion (constants)
# ---------------------------------------------------------
# region FUNCTIONS


def print_tree(top_node: 'ASTNode', meaning: Optional[str] = None, to_filepath: Optional[str] = None):
    full_tree_lines: List[str] = []
    top_node.print(None, '', "AST root" if not meaning else meaning, True, full_tree_lines)
    lines = '\n'.join(full_tree_lines)
    if to_filepath:
        with open(to_filepath, 'w', encoding='utf-8') as output:
            print(lines, file=output)
    else:
        print(lines)
            

# endregion (functions)
# ---------------------------------------------------------
# region CLASSES


# region AstNode

class ASTNode:

    def __str__(self):
        return f": {self._node_name} :"

    def __repr__(self):
        return f"{self.__class__.__qualname__}()"

    @property
    def _node_name(self) -> str:
        return self.__class__.__name__.replace('Node', '')

    def _node_title(self) -> str:
        return self._node_name

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        pass

    def print(self, parent: Optional['ASTNode'], depth: str, meaning: Optional[str] = None, is_last_child: bool = False,
              output: Optional[List[str]] = None) -> None:
        leaf: str
        if parent:
            leaf = ' └─ ' if is_last_child else ' ├─ '
        else:
            leaf = ' *─ '

        title_meaning: str = f" as {meaning}" if meaning else ''
        line = f"{depth}{leaf}{self._node_title()}{title_meaning}"
        if output is not None:
            output.append(line)

        self._print_leves(f"{depth}{'    ' if is_last_child else ' │  '}", output)


class SourceNode(ASTNode):

    def __init__(self, location: Any):
        self.location: Any = location   # Todo: define and set actual attribute type


# endregion (AstNode)

# region Assembly Nodes


class AsmbNode(ASTNode):

    def __init__(self):
        self.modules: Dict[str, ModuleNode] = {}
        self.src_dir: str = ''
        self.dst_dir: str = ''

    def __getitem__(self, key: str) -> 'ModuleNode':
        return self.modules.__getitem__(key)

    def __setitem__(self, key: str, value: 'ModuleNode') -> None:
        self.modules.__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        self.modules.__delitem__(key)


class ModuleNode(ASTNode):

    def __init__(self, fname: str, scope: Optional['ModuleScopeNode'] = None):
        self.fname: str = fname
        self.resolved: bool = False
        self.resolving: bool = False
        self.scope: Optional['ModuleScopeNode'] = scope

# endregion (assembly nodes)

# region Template Node


class TemplNode(SourceNode):

    def __init__(self, location: Any, typenames: List[str], sizes: Dict[str, 'ExprNode']):
        super().__init__(location)
        self.typenames: List[str] = typenames
        self.sizes: Dict[str, ExprNode] = sizes
        self.subject: Optional[TyclNode] = None

# endregion (template node)

# region (Declaration Nodes)


class DeclNode(SourceNode):

    def __init__(self, location: Any, declname: str, decltype: 'TypeNode', exports: bool = False):
        super().__init__(location)
        self.exports: bool = exports
        self.name: str = declname
        self.type: TypeNode = decltype

    def _node_title(self) -> str:
        return f"{'[exp]' if self.exports else ''} {self._node_name} :: {self.name} : {self.type.name}"


class VarDeclNode(DeclNode):
    """Variable declaration node.

    :ivar value: the ExprNode that initializes the variable
    :ivar offset: the frame offset in bytes
    """

    def __init__(self, location: Any, offset: int, declname: str, decltype: 'TypeNode',
                 declvalue: Optional['ExprNode'] = None):
        super().__init__(location, declname, decltype)
        self.value: Optional['ExprNode'] = declvalue
        self.offset: DeclOffset = DeclOffset(offset, 1)

    def _node_title(self) -> str:
        return (
            f"{'[exp]' if self.exports else ''} {self._node_name} ::"
            f" {self.name} : {self.type.name} (Offs: {self.offset.index})"
        )

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        if self.value:
            self.value.print(self, depth, 'value', True, output)


class ConstDeclNode(DeclNode):

    def __init__(self, location: Any, declname: str, decltype: 'TypeNode', declvalue: 'ExprNode',
                 exports: bool = False):
        super().__init__(location, declname, decltype, exports)
        self.value: ExprNode = declvalue

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        if self.value:
            self.value.print(self, depth, 'value', True, output)


class EnumDeclNode(DeclNode):

    def __init__(self, location: Any, declname: str, decltype: 'TypeNode', declvalue: 'ExprNode'):
        super().__init__(location, declname, decltype, decltype.exports)
        self.value: ExprNode = declvalue

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        if self.value:
            self.value.print(self, depth, 'value', True, output)


class FunctionDeclNode(DeclNode):

    def __init__(self, location: Any, offset: int, declname: str, decltype: 'TypeNode',
                 params: Dict[str, 'ParamDeclNode'], scope: 'FunctionScopeNode', exports: bool = False):
        super().__init__(location, declname, decltype, exports)
        self.template: Optional[TemplNode] = None
        self.defined: bool = False
        self.offset: DeclOffset = DeclOffset(offset, 1)
        self.params: Dict[str, ParamDeclNode] = params
        self.type: TypeNode = decltype
        self.scope: FunctionScopeNode = scope

    def _node_title(self) -> str:
        return (
            f"{'[exp]' if self.exports else ''} {self._node_name} ::"
            f" {self.name} : {self.type.name} (Params: {len(self.params)})"
        )

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        if self.template:
            self.template.print(self, depth, 'template', False, output)
        for i, param in enumerate(self.params):
            self.params[param].print(self, depth, f'param {i}', False, output)
        self.scope.print(self, depth, 'body', True, output)


class ParamDeclNode(DeclNode):

    def __init__(self, location: Any, offset: int, declname: str, decltype: 'TypeNode', has_default: bool = False,
                 declvalue: Optional['ExprNode'] = None):
        super().__init__(location, declname, decltype)
        self.offset: DeclOffset = DeclOffset(offset, 1)
        self.has_default: bool = has_default
        self.default_value: Optional['ExprNode'] = declvalue

    def _node_title(self) -> str:
        return f"{self._node_name} :: {self.name} : {self.type.name} (Offs: {self.offset.index})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        if self.has_default:
            self.default_value.print(self, depth, 'default value', True, output)


class FieldDeclNode(DeclNode):

    def __init__(self, location: Any, offset: int, thisdecl: 'TyclNode', declname: str, decltype: 'TypeNode',
                 has_default: bool = False, declvalue: Optional['ExprNode'] = None):
        super().__init__(location, declname, decltype)
        self.thisdecl: TyclNode = thisdecl
        self.offset: DeclOffset = DeclOffset(offset, 1)
        self.has_default: bool = has_default
        self.default_value: Optional['ExprNode'] = declvalue

    def _node_title(self) -> str:
        return f"{self._node_name} :: {self.name} : {self.type.name} (Offs: {self.offset.index})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        if self.has_default:
            self.default_value.print(self, depth, 'default value', True, output)


class PropertyDeclNode(DeclNode):

    def __init__(self, location: Any, thisdecl: 'TyclNode', declname: str, decltype: 'TypeNode'):
        super().__init__(location, declname, decltype)
        self.thisdecl: TyclNode = thisdecl
        self.getterstmt: Optional[GetterStmtNode] = None
        self.setterstmt: Optional[SetterStmtNode] = None

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        if self.getterstmt:
            self.getterstmt.print(self, depth, 'getter', self.setterstmt is None, output)
        if self.setterstmt:
            self.setterstmt.print(self, depth, 'setter', True, output)


class MethodDeclNode(DeclNode):

    def __init__(self, location: Any, offset: int, thisdecl: 'TyclNode', declname: str, decltype: 'TypeNode',
                 params: Dict[str, ParamDeclNode], scope: 'MethodScopeNode', operator: bool = False):
        super().__init__(location, declname, decltype)
        self.thisdecl: TyclNode = thisdecl
        self.defined: bool = False
        self.is_operator: bool = operator
        self.offset: DeclOffset = DeclOffset(offset, 1)
        self.params: Dict[str, ParamDeclNode] = params
        self.type: TypeNode = decltype
        self.scope: MethodScopeNode = scope

    def _node_title(self) -> str:
        return f"{self._node_name} :: {self.name} : {self.type.name} (Params: {len(self.params)})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        for i, param in enumerate(self.params):
            self.params[param].print(self, depth, f'param {i}', False, output)
        self.scope.print(self, depth, 'body', True, output)

# endregion (declaration nodes)

# region Type Nodes


class TypeNode(SourceNode):

    def __init__(self, location: Any, typename: Optional[str], exports: bool = False):
        super().__init__(location)
        self.exports: bool = exports
        self.name: Optional[str] = typename

    def _node_title(self) -> str:
        return f"{'[exp]' if self.exports else ''} {self._node_name} :: {self.name}"


class PrimitiveTypeNode(TypeNode):

    def __init__(self, location: Any, typename: str):
        super().__init__(location, typename)


# region Primitive Types


class IntegerTypeNode(PrimitiveTypeNode):

    def __init__(self, location: Any, typename: str, bytesize: int, signed: bool):
        super().__init__(location, typename)
        self.bytesize: int = bytesize
        self.signed: bool = signed


class FloatTypeNode(PrimitiveTypeNode):

    def __init__(self, location: Any, typename: str, bytesize: int):
        super().__init__(location, typename)
        self.bytesize: int = bytesize


class StringTypeNode(PrimitiveTypeNode):

    def __init__(self, location: Any, typename: str):
        super().__init__(location, typename)

# endregion (primitive types)


class EnumTypeNode(TypeNode):

    def __init__(self, location: Any, typename: str, basetype: TypeNode, is_flagset: bool, exports: bool = False):
        super().__init__(location, typename, exports)
        self.basetype: TypeNode = basetype
        self.is_flagset: bool = is_flagset

    def _node_title(self) -> str:
        return (f"{'[exp]' if self.exports else ''} {self._node_name} :: {self.name} "
                f"(Base: {self.basetype.name}, {'Flags' if self.is_flagset else ''})")


class SignatureTypeNode(TypeNode):

    def __init__(self, location: Any, typename: str, paramtypes: List[Union[TypeNode, 'TyclNode']],
                 restype: Union[TypeNode, 'TyclNode'], exports: bool = False):
        super().__init__(location, typename, exports)
        self.paramtypes: List[Union[TypeNode, 'TyclNode']] = paramtypes
        self.restype: Union[TypeNode, 'TyclNode'] = restype

    def _node_title(self) -> str:
        return (f"{'[exp]' if self.exports else ''} {self._node_name} :: {self.name} : {self.restype.name} "
                f"(Params: {len(self.paramtypes)})")


class PointerTypeNode(TypeNode):

    def __init__(self, location: Any, basetype: Union[TypeNode, 'TyclNode']):
        super().__init__(location, None)
        self.basetype: Union[TypeNode, TyclNode] = basetype

    def _node_title(self) -> str:
        return f"{self._node_name} :: {self.name} (Base: {self.basetype.name})"


class ArrayTypeNode(TypeNode):

    def __init__(self, location: Any, basetype: Union[TypeNode, 'TyclNode'], sizeexpr: Optional['ExprNode'] = None):
        super().__init__(location, None)
        self.basetype: Union[TypeNode, TyclNode] = basetype
        self.sizeexpr: Optional[ExprNode] = sizeexpr

    def _node_title(self) -> str:
        return f"{self._node_name} :: {self.name} (Base: {self.basetype.name})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        if self.sizeexpr:
            self.sizeexpr.print(self, depth, 'length', True, output)


class AliasTypeNode(TypeNode):

    def __init__(self, location: Any, typename: str, basetype: Union[TypeNode, 'TyclNode'], exports: bool = False):
        super().__init__(location, typename, exports)
        self.basetype: Union[TypeNode, TyclNode] = basetype

    def _node_title(self) -> str:
        return f"{self._node_name} :: {self.name} (Base: {self.basetype.name})"


class ExceptionTypeNode(TypeNode):

    def __init__(self, location: Any, typename: str, basetype: Optional['ExceptionTypeNode'], exports: bool = False):
        super().__init__(location, typename, exports)
        self.basetype: Optional[ExceptionTypeNode] = basetype

    def _node_title(self) -> str:
        return f"{self._node_name} :: {self.name} (Base: {self.basetype.name})"


# endregion (type nodes)

# region TypeDeclaration Nodes


class TyclNode(SourceNode):

    def __init__(self, location: Any, tyclname: str, exports: bool = False):
        super().__init__(location)
        self.exports: bool = exports
        self.name: str = tyclname
        self.fields: Dict[str, FieldDeclNode] = {}
        self.properties: Dict[str, PropertyDeclNode] = {}
        self.methods: Dict[str, MethodDeclNode] = {}
        self.operators: Dict[str, MethodDeclNode] = {}
        self.members: List[str] = []

    def __getitem__(self, key: str) -> Union[FieldDeclNode, PropertyDeclNode, MethodDeclNode]:
        if key in self.members:
            if key in self.fields:
                return self.fields.get(key)
            elif key in self.properties:
                return self.properties.get(key)
            else:
                return self.methods.get(key)
        else:
            raise KeyError(f"Not found: '{key}'")

    def __contains__(self, item: str) -> bool:
        return self.members.__contains__(item)

    def declare(self, declnode: Union[FieldDeclNode, PropertyDeclNode, MethodDeclNode]) -> bool:
        if declnode.name in self.members:
            return False

        if isinstance(declnode, FieldDeclNode):
            self.fields[declnode.name] = declnode
        elif isinstance(declnode, PropertyDeclNode):
            self.properties[declnode.name] = declnode
        elif isinstance(declnode, MethodDeclNode):
            if declnode.is_operator:
                self.operators[declnode.name] = declnode
            else:
                self.methods[declnode.name] = declnode
        else:
            return False

        self.members.append(declnode.name)
        return True

    def _node_title(self) -> str:
        return f"{'[exp]' if self.exports else ''} {self._node_name} :: {self.name}"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        nfields = len(self.fields)
        nprops = len(self.properties)
        nmethods = len(self.methods)
        nopers = len(self.operators)
        for i, name in enumerate(self.fields):
            self.fields[name].print(self, depth, 'field', i == nfields - 1 and (nprops + nmethods + nopers == 0),
                                    output)
        for i, name in enumerate(self.properties):
            self.properties[name].print(self, depth, 'property', i == nfields - 1 and (nmethods + nopers == 0), output)
        for i, name in enumerate(self.methods):
            self.methods[name].print(self, depth, 'method', i == nfields - 1 and nopers == 0, output)
        for i, name in enumerate(self.operators):
            self.operators[name].print(self, depth, 'operator overload', i == nfields - 1 and nopers == 0, output)


class StructureTyclNode(TyclNode):
    pass


class InterfaceTyclNode(TyclNode):
    pass


class ClassTyclNode(TyclNode):

    def __init__(self, location: Any, tyclname: str, exports: bool = False, baseclass: Optional[TyclNode] = None):
        super().__init__(location, tyclname, exports)
        self.baseclass: Optional[TyclNode] = baseclass

    def _node_title(self) -> str:
        return (f"{'[exp]' if self.exports else ''} {self._node_name} :: {self.name}"
                f" (Base: {self.baseclass.name if self.baseclass else ''})")


class SingletonTyclNode(TyclNode):
    pass


# endregion (typedeclaration nodes)

# region Scope Nodes


class ScopeNode(SourceNode):
    """Scope Node base class."""

    def __init__(self, location: Any, basescope: Optional['ScopeNode'] = None):
        super().__init__(location)
        self.labels: Dict[str, 'StmtNode'] = {}
        self.basescope: Optional[ScopeNode] = basescope
        self.declarations: Dict[str, DeclNode] = {}

    def has_label(self, label: str) -> bool:
        if label in self.labels:
            return True
        elif self.basescope:
            return self.basescope.has_label(label)
        else:
            return False

    def define_label(self, label: str) -> str:
        pass

    def get_stmt(self, label: str) -> Optional['StmtNode']:
        pass

    def set_stmt(self, label: str, stmtnode: 'StmtNode') -> None:
        pass

    def has_declared(self, name: str) -> bool:
        """Returns whether the given name is declared in the current scope."""
        return self.declarations.__contains__(name)

    def name_exists(self, name: str) -> bool:
        """Returns whether the given name exists in the enclosing scopes."""
        if self.has_declared(name):
            return True
        elif self.basescope:
            return self.basescope.name_exists(name)
        else:
            return False

    def get_name(self, name: str) -> Optional[Union['DeclNode', 'TyclNode']]:
        if self.has_declared(name):
            return self.declarations.get(name)
        elif self.basescope:
            return self.basescope.get_name(name)
        else:
            return None

    def declare(self, declnode: Union['DeclNode', 'TyclNode', 'TypeNode'], *expected_scopes: Type['ScopeNode']) -> bool:
        if self.has_declared(declnode.name):
            return False

        self.declarations[declnode.name] = declnode
        base: Optional[ScopeNode] = self.find_scope(*expected_scopes)
        if not base:
            return False

    def find_scope(self, *expected_scopes: Type['ScopeNode']) -> Optional['ScopeNode']:
        if self.__class__ in expected_scopes:
            return self
        elif self.basescope:
            return self.basescope.find_scope(*expected_scopes)
        else:
            return None

    def _node_title(self) -> str:
        return f"{self._node_name} :: Scope"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        nvars: int = len(self.declarations)
        for i, name in enumerate(self.declarations):
            self.declarations[name].print(self, depth, 'declaration', i == nvars - 1)


class BasicScopeNode(ScopeNode):

    def __init__(self, location: Any, basescope: Optional['ScopeNode'] = None):
        super().__init__(location, basescope)
        self.statements: List[StmtNode] = []

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        nvars: int = len(self.declarations)
        ninstr: int = len(self.statements)
        for i, name in enumerate(self.declarations):
            self.declarations[name].print(self, depth, 'declaration', i == nvars - 1 and ninstr == 0)
        for i, instr in enumerate(self.statements):
            instr.print(self, depth, 'statement', i == ninstr - 1, output)


class ModuleScopeNode(ScopeNode):
    pass


class FunctionScopeNode(BasicScopeNode):
    pass


class MethodScopeNode(BasicScopeNode):
    pass


class PropertyScopeNode(BasicScopeNode):
    pass


class LoopScopeNode(BasicScopeNode):
    pass


class CaseScopeNode(BasicScopeNode):
    pass


class TryScopeNode(BasicScopeNode):
    pass

# endregion (scope nodes)

# region Statement Nodes


class StmtNode(SourceNode):

    def __init__(self, location: Any):
        super().__init__(location)

    def _node_title(self) -> str:
        return f"{self._node_name}"


class AssignmentStmtNode(StmtNode):

    def __init__(self, location: Any, exprlvalue: 'LValueExprNode', exprvalue: 'ExprNode'):
        super().__init__(location)
        self.exprlvalue: LValueExprNode = exprlvalue
        self.exprvalue: ExprNode = exprvalue

    def _node_title(self) -> str:
        return f"{self._node_name} :: Assignment"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.exprlvalue.print(self, depth, 'target', False, output)
        self.exprvalue.print(self, depth, 'value', True, output)


class UnpackStmtNode(StmtNode):

    def __init__(self, location: Any):
        super().__init__(location)
        # TODO: take a look the syntax for this node and check what it needs


class ExpressionStmtNode(StmtNode):

    def __init__(self, location: Any, expr: Union['UnaryExprNode', 'DirectCallExprNode', 'IndirectCallExprNode']):
        super().__init__(location)
        self.expr: Union['UnaryExprNode', 'DirectCallExprNode', 'IndirectCallExprNode'] = expr

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.expr.print(self, depth, 'expression', True, output)


class GetterStmtNode(StmtNode):

    def __init__(self, location: Any, getterscope: PropertyScopeNode):
        super().__init__(location)
        self.scope: PropertyScopeNode = getterscope

    def _node_title(self) -> str:
        return f"{self._node_name} :: Getter"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.scope.print(self, depth, 'statement body', True, output)


class SetterStmtNode(StmtNode):

    def __init__(self, location: Any, setterscope: PropertyScopeNode):
        super().__init__(location)
        self.scope: PropertyScopeNode = setterscope

    def _node_title(self) -> str:
        return f"{self._node_name} :: Setter"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.scope.print(self, depth, 'statement body', True, output)


class IfThenStmtNode(StmtNode):

    def __init__(self, location: Any, condexpr: 'ExprNode', thenscope: BasicScopeNode):
        super().__init__(location)
        self.condexpr: ExprNode = condexpr
        self.thenscope: BasicScopeNode = thenscope

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.condexpr.print(self, depth, 'condition', False, output)
        self.thenscope.print(self, depth, 'then scope', True, output)


class IfElseStmtNode(StmtNode):

    def __init__(self, location: Any, condexpr: 'ExprNode', thenscope: BasicScopeNode, elsescope: BasicScopeNode):
        super().__init__(location)
        self.condexpr: ExprNode = condexpr
        self.thenscope: BasicScopeNode = thenscope
        self.elsescope: BasicScopeNode = elsescope

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.condexpr.print(self, depth, 'condition', False, output)
        self.thenscope.print(self, depth, 'then scope', False, output)
        self.elsescope.print(self, depth, 'else scope', True, output)


class WhileStmtNode(StmtNode):

    def __init__(self, location: Any, condexpr: 'ExprNode', loopscope: LoopScopeNode, label: Optional[str] = None):
        super().__init__(location)
        self.condexpr: ExprNode = condexpr
        self.scope: LoopScopeNode = loopscope
        self.label: Optional[str] = label

    def _node_title(self) -> str:
        return f"{self._node_name} :: (Label: {self.label})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.condexpr.print(self, depth, 'condition', False, output)
        self.scope.print(self, depth, 'loop scope', True, output)


class DoWhileStmtNode(StmtNode):

    def __init__(self, location: Any, condexpr: 'ExprNode', loopscope: LoopScopeNode, label: Optional[str] = None):
        super().__init__(location)
        self.condexpr: ExprNode = condexpr
        self.scope: LoopScopeNode = loopscope
        self.label: Optional[str] = label

    def _node_title(self) -> str:
        return f"{self._node_name} :: (Label: {self.label})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.condexpr.print(self, depth, 'condition', False, output)
        self.scope.print(self, depth, 'loop scope', True, output)


class DoUntilStmtNode(StmtNode):

    def __init__(self, location: Any, condexpr: 'ExprNode', loopscope: LoopScopeNode, label: Optional[str] = None):
        super().__init__(location)
        self.condexpr: ExprNode = condexpr
        self.scope: LoopScopeNode = loopscope
        self.label: Optional[str] = label

    def _node_title(self) -> str:
        return f"{self._node_name} :: (Label: {self.label})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.condexpr.print(self, depth, 'condition', False, output)
        self.scope.print(self, depth, 'loop scope', True, output)


class RepeatStmtNode(StmtNode):

    def __init__(self, location: Any, startdecls: 'VarDeclNode', stopexprs: 'ExprNode', stepstmts: 'AssignmentStmtNode',
                 loopscope: LoopScopeNode, label: Optional[str] = None):
        super().__init__(location)
        self.startdecl: VarDeclNode = startdecls
        self.stopexpr: ExprNode = stopexprs
        self.stepstmt: AssignmentStmtNode = stepstmts
        self.scope: LoopScopeNode = loopscope
        self.label: Optional[str] = label

    def _node_title(self) -> str:
        return f"{self._node_name} :: (Label: {self.label})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.stopexpr.print(self, depth, 'counter expression', False, output)
        self.scope.print(self, depth, 'loop scope', True, output)


class ForStmtNode(StmtNode):

    def __init__(self, location: Any, startdecls: List['VarDeclNode'], stopexprs: List['ExprNode'],
                 stepstmts: List['ExpressionStmtNode'], loopscope: LoopScopeNode, label: Optional[str] = None):
        super().__init__(location)
        self.startdecls: List[VarDeclNode] = startdecls
        self.stopexprs: List[ExprNode] = stopexprs
        self.stepstmts: List[ExpressionStmtNode] = stepstmts
        self.scope: LoopScopeNode = loopscope
        self.label: Optional[str] = label

    def _node_title(self) -> str:
        return f"{self._node_name} :: (Label: {self.label})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        for decl in self.startdecls:
            decl.print(self, depth, 'loop init', False, output)
        for expr in self.stopexprs:
            expr.print(self, depth, 'loop conditions', False, output)
        for stmt in self.stepstmts:
            stmt.print(self, depth, 'loop step')
        self.scope.print(self, depth, 'loop scope', True, output)


class ForEachStmtNode(StmtNode):

    def __init__(self, location: Any, elmtdecl: VarDeclNode, setexpr: 'ExprNode', loopscope: LoopScopeNode,
                 label: Optional[str] = None):
        super().__init__(location)
        self.element: VarDeclNode = elmtdecl
        self.container: ExprNode = setexpr
        self.scope: LoopScopeNode = loopscope
        self.label: Optional[str] = label

    def _node_title(self) -> str:
        return f"{self._node_name} :: (Label: {self.label})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.element.print(self, depth, 'loop item', False, output)
        self.container.print(self, depth, 'loop container', False, output)
        self.scope.print(self, depth, 'loop scope', True, output)


class SwitchStmtNode(StmtNode):

    def __init__(self, location: Any, targetexpr: 'NameExprNode', stmtcases: List['CaseStmtNode'],
                 label: Optional[str] = None):
        super().__init__(location)
        self.cases: List[CaseStmtNode] = stmtcases
        self.targetexpr: NameExprNode = targetexpr
        self.label: Optional[str] = label

    def _node_title(self) -> str:
        return f"{self._node_name} :: {self.targetexpr.name} : (Label: {self.label})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.targetexpr.print(self, depth, 'target', False, output)
        ncases: int = len(self.cases)
        for i, case in enumerate(self.cases):
            case.print(self, depth, 'case', i == ncases - 1, output)


class CaseStmtNode(StmtNode):

    def __init__(self, location: Any, caseexpr: List['ExprNode'], casescope: CaseScopeNode, is_default: bool = False):
        super().__init__(location)
        self.cases: List[ExprNode] = caseexpr
        self.scope: CaseScopeNode = casescope
        self.is_default: bool = is_default

    def _node_title(self) -> str:
        return f"{self._node_name} :: Constant expression"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        for caseexpr in self.cases:
            caseexpr.print(self, depth, 'target', False, output)
        self.scope.print(self, depth, 'case scope', True, output)


class TryStmtNode(StmtNode):

    def __init__(self, location: Any, stmtclauses: List['ExceptClauseStmtNode'], tryscope: TryScopeNode):
        super().__init__(location)
        self.clauses: List[ExceptClauseStmtNode] = stmtclauses
        self.scope: TryScopeNode = tryscope

    def _node_title(self) -> str:
        return f"{self._node_name} :: Try"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        for exception in self.clauses:
            exception.print(self, depth, None, False, output)
        self.scope.print(self, depth, 'rescue scope', True, output)


class ExceptClauseStmtNode(StmtNode):

    def __init__(self, location: Any, catches: List['ExceptionNameExprNode'], xcptscope: ScopeNode):
        super().__init__(location)
        self.catches: List[ExceptionNameExprNode] = catches
        self.scope: ScopeNode = xcptscope

    def _node_title(self) -> str:
        return f"{self._node_name} :: Clause"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        for exception in self.catches:
            exception.print(self, depth, 'exception', False, output)
        self.scope.print(self, depth, 'rescue scope', True, output)


class RaiseStmtNode(StmtNode):

    def __init__(self, location: Any, xcptexpr: 'ExceptionNameExprNode'):
        super().__init__(location)
        self.xcptexpr: ExceptionNameExprNode = xcptexpr


class ImportStmtNode(StmtNode):
    pass


class BreakStmtNode(StmtNode):

    def __init__(self, location: Any, stmtlabel: Optional[str] = None):
        super().__init__(location)
        self.stmtlabel: Optional[str] = stmtlabel

    def _node_title(self) -> str:
        label: str = f" :: (Label: {self.stmtlabel})" if self.stmtlabel else ''
        return f"{self._node_name}{label}"


class ContinueStmtNode(StmtNode):

    def __init__(self, location: Any, stmtlabel: Optional[str] = None):
        super().__init__(location)
        self.stmtlabel: Optional[str] = stmtlabel

    def _node_title(self) -> str:
        label: str = f" :: (Label: {self.stmtlabel})" if self.stmtlabel else ''
        return f"{self._node_name}{label}"


class ReturnStmtNode(StmtNode):

    def __init__(self, location: Any, exprvalue: Optional['ExprNode'] = None):
        super().__init__(location)
        self.valueexpr: Optional[ExprNode] = exprvalue

    def _node_title(self) -> str:
        return f"{self._node_name}"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.valueexpr.print(self, depth, 'return value', False, output)

# endregion (statement nodes)

# region Expression Nodes


class ExprNode(SourceNode):

    def __init__(self, location: Any):
        super().__init__(location)

    def _node_title(self) -> str:
        return f"{self._node_name}"


class LiteralExprNode(ExprNode):

    def __init__(self, location: Any, value: Union[str, int, float], valuetype: TypeNode):
        super().__init__(location)
        self.value: Union[str, int, float] = value
        self.type: TypeNode = valuetype

    def _node_title(self) -> str:
        return f"{self._node_name} :: {self.type.name}"


class NameExprNode(ExprNode):

    def __init__(self, location: Any, name: str):
        super().__init__(location)
        self.name: str = name

    def _node_title(self) -> str:
        return f"{self._node_name} :: {self.name}"


# region Name Expressions


class VarNameExprNode(NameExprNode):
    pass


class ConstNameExprNode(NameExprNode):
    pass


class ParamNameExprNode(NameExprNode):
    pass


class FunctionNameExprNode(NameExprNode):
    pass


class FieldNameExprNode(NameExprNode):
    pass


class PropertyNameExprNode(NameExprNode):
    pass


class EnumNameExprNode(NameExprNode):
    pass


class StructNameExprNode(NameExprNode):
    pass


class ClassNameExprNode(NameExprNode):
    pass


class ExceptionNameExprNode(NameExprNode):
    pass

# endregion (name expressions)


class UnaryExprNode(ExprNode):

    def __init__(self, location: Any, operand: ExprNode):
        super().__init__(location)
        self.operand: ExprNode = operand

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.operand.print(self, depth, 'operand', True, output)


# region Unary Expressions


class IncrUnaryExprNode(UnaryExprNode):

    def __init__(self, location: Any, operand: ExprNode, is_post: bool):
        super().__init__(location, operand)
        self.is_post: bool = is_post

    def _node_title(self) -> str:
        return f"{self._node_name} :: {'(expr)++' if self.is_post else '++(expr)'}"


class DecrUnaryExprNode(UnaryExprNode):

    def __init__(self, location: Any, operand: ExprNode, is_post: bool):
        super().__init__(location, operand)
        self.is_post: bool = is_post

    def _node_title(self) -> str:
        return f"{self._node_name} :: {'(expr)--' if self.is_post else '--(expr)'}"


class NegateUnaryExprNode(UnaryExprNode):

    def _node_title(self) -> str:
        return f"{self._node_name} :: ~(expr)"


class ReferenceUnaryExprNode(UnaryExprNode):

    def _node_title(self) -> str:
        return f"{self._node_name} :: &(expr)"


class DereferenceUnaryExprNode(UnaryExprNode):

    def _node_title(self) -> str:
        return f"{self._node_name} :: *(expr)"


class UnpackUnaryExprNode(UnaryExprNode):
    pass

# endregion (unary expressions)


class BinaryExprNode(ExprNode):

    def __init__(self, location: Any, leftexpr: ExprNode, rightexpr: ExprNode, operator: str, is_inplace: bool = False):
        super().__init__(location)
        self.left: ExprNode = leftexpr
        self.right: ExprNode = rightexpr
        self.operator: str = operator
        self.is_inplace: bool = is_inplace

    def _node_title(self) -> str:
        return f"{self._node_name} :: (expr) {self.operator} (expr)"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.left.print(self, depth, 'left operand', False, output)
        self.right.print(self, depth, 'right operand', True, output)


# region Binary Expressions


class MultBinaryExprNode(BinaryExprNode):
    pass


class AddBinaryExprNode(BinaryExprNode):
    pass


class CompareBinaryExprNode(BinaryExprNode):
    pass


class AndBinaryExprNode(BinaryExprNode):
    pass


class OrBinaryExprNode(BinaryExprNode):
    pass

# endregion (binary expressions)


class TernaryExprNode(ExprNode):

    def __init__(self, location: Any, condition: ExprNode, thenexpr: ExprNode, elseexpr: ExprNode):
        super().__init__(location)
        self.condition: ExprNode = condition
        self.thenexpr: ExprNode = thenexpr
        self.elseexpr: ExprNode = elseexpr

    def _node_title(self) -> str:
        return f"{self._node_name} :: (expr) ? (expr) : (expr)"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.condition.print(self, depth, 'ternary condition', True, output)
        self.thenexpr.print(self, depth, 'then expression', True, output)
        self.elseexpr.print(self, depth, 'else expression', False, output)


class DirectCallExprNode(ExprNode):

    def __init__(self, location: Any, funcnameexpr: FunctionNameExprNode, arglist: List[ExprNode]):
        super().__init__(location)
        self.funcnameexpr: FunctionNameExprNode = funcnameexpr
        self.arglist: List[ExprNode] = arglist

    def _node_title(self) -> str:
        return f"{self._node_name} :: {self.funcnameexpr}(...) : (Args: {len(self.arglist)})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        nargs: int = len(self.arglist)
        for i, arg in enumerate(self.arglist):
            arg.print(self, depth, 'call argument expression', i == nargs - 1, output)


class IndirectCallExprNode(ExprNode):

    def __init__(self, location: Any, callableexpr: ExprNode, arglist: List[ExprNode]):
        super().__init__(location)
        self.callableexpr: ExprNode = callableexpr
        self.arglist: List[ExprNode] = arglist

    def _node_title(self) -> str:
        return f"{self._node_name} :: (expr)(...) : (Args: {len(self.arglist)})"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.callableexpr.print(self, depth, 'callable expression', False, output)
        nargs: int = len(self.arglist)
        for i, arg in enumerate(self.arglist):
            arg.print(self, depth, 'call argument expression', i == nargs - 1, output)


class IndexExprNode(ExprNode):

    def __init__(self, location: Any, baseexpr: ExprNode, indexexpr: ExprNode):
        super().__init__(location)
        self.baseexpr: ExprNode = baseexpr
        self.indexexpr: ExprNode = indexexpr

    def _node_title(self) -> str:
        return f"{self._node_name} :: (expr)[(expr)]"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.baseexpr.print(self, depth, 'base expression', False, output)
        self.indexexpr.print(self, depth, 'index expression', True, output)


class MemberExprNode(ExprNode):

    def __init__(self, location: Any, baseexpr: ExprNode, memberexpr: NameExprNode):
        super().__init__(location)
        self.baseexpr: ExprNode = baseexpr
        self.memberexpr: NameExprNode = memberexpr

    def _node_title(self) -> str:
        return f"{self._node_name} :: (expr).{self.memberexpr.name}"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.baseexpr.print(self, depth, 'base expression', False, output)


class AggregateExprNode(ExprNode):

    def __init__(self, location: Any, exprlist: List[ExprNode]):
        super().__init__(location)
        self.exprlist: List[ExprNode] = exprlist

    def _node_title(self) -> str:
        return f"{self._node_name} :: {{(expr), ... }}"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        nexpr: int = len(self.exprlist)
        for i, expr in enumerate(self.exprlist):
            expr.print(self, depth, 'aggregate element expression', i == nexpr - 1, output)


class LValueExprNode(ExprNode):

    def __init__(self, location: Any, exprtarget: ExprNode):
        super().__init__(location)
        self.exprtarget: ExprNode = exprtarget

    def _node_title(self) -> str:
        return f"{self._node_name} :: (expr)"

    def _print_leves(self, depth: str, output: Optional[List[str]] = None):
        self.exprtarget.print(self, depth, 'L-Value expression', True, output)

# endregion (expression nodes)

# endregion (classes)
# ---------------------------------------------------------
# region BASIC TEST


if __name__ == '__main__':
    i32 = IntegerTypeNode(0, 'i32', 4, True)
    node = AddBinaryExprNode(
        0,
        IncrUnaryExprNode(0, LiteralExprNode(0, 127, i32), True),
        MultBinaryExprNode(0, LiteralExprNode(0, 255, i32), VarNameExprNode(0, 'x'), '*'),
        '+'
    )
    print_tree(node, 'basic multiplication', '../scrap/ast_output.txt')

    # allnames = []
    #
    # for name in sorted(globals().copy().keys()):
    #     if name.endswith('Node'):
    #         allnames.append(name)
    # print("',\n    '".join(allnames))

# endregion (basic test)
