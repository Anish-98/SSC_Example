from algosdk.future.transaction import OnComplete
from pyteal import *
from pyteal.ast.expr import Expr
from pyteal.ast.global_ import Global
from pyteal.ast.itxn import InnerTxn, InnerTxnBuilder
from pyteal.ast.return_ import Approve, Reject
from pyteal.ast.subroutine import Subroutine
from pyteal.ast.txn import Txn, TxnField, TxnType
from pyteal.types import TealType
from utils.statehelper import GlobalState, LocalState

def approval_program():
  var_a = GlobalState('A')
  var_b = GlobalState ('B')
  var_add_res = GlobalState('add_res')
  var_sub_res = GlobalState('sub_res')
  user_res_store = LocalState('res')

  on_create = Seq(
    var_a.put(Int(0)),
    var_b.put(Int(0)),
    var_add_res.put(Int(0)),
    var_sub_res.put(Int(0)),
    Approve()   # approve is just Int(1) which is permissive 
                # reject is just Int(0) which rejects any logic
  )

  # 0th index of application args will be command you want to be executed
  # from 1st onwards consider it as arguments

  @Subroutine(TealType.uint64)
  def add_two_variables(a:Expr,b:Expr) -> Expr:
    return a + b

  @Subroutine(TealType.uint64)
  def sub_two_variables(a:Expr,b:Expr) -> Expr:
    return a - b

  user_optin = Seq(
    user_res_store.put(Int(0)),
    Approve()
  )
  
  #ip - input
  ip_a = Btoi(Txn.application_args[1])   
  ip_b = Btoi(Txn.application_args[2])
  on_add = Seq(
    var_a.put(ip_a),
    var_b.put(ip_b),
    var_add_res.put(ip_a + ip_b),
    user_res_store.put(var_add_res.get()),
    # var_add_res.put(add_two_variables(ip_a,ip_b))
    Approve()
  )
  on_sub = Seq(
    var_a.put(ip_a),
    var_b.put(ip_b),
    If(ip_a > ip_b).
    Then(      
      var_sub_res.put(ip_a - ip_b) #if there are multiple things you want to impose or execute in Then 
                                   #then use Seq()
    ).
    Else(
      Reject()
    ),
    # var_sub_res.put(sub_two_variables(ip_a,ip_b)),
    Approve()
  )
  

  on_call_method = Txn.application_args[0]
  on_call = Cond(
    [on_call_method == Bytes("ADD"), on_add],
    [on_call_method == Bytes("SUB"), on_sub],
  )

  program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.NoOp, on_call],
        [Txn.on_completion() == OnComplete.OptIn, user_optin],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(Int(1))],
    )
  
  return program

def clear_state_program():
  return Seq(
    Approve()    # approve is equivalent to Int(1)/true.
  )


if __name__== "__main__":
  compiled_teal = compileTeal(approval_program(), mode=Mode.Application, version=5)
  print(compiled_teal)

