from  arm_robot_bridge import ArmRobot
import time
if __name__ == "__main__":
    robot = ArmRobot()
 
    """状態の確認"""
    # print("error:", robot.error)
    # print("status:", robot.status)
    # print("task_run:", robot.taskrun)
    # print("emergency_stop",robot.emergency_stop)
    print("temp:", robot.temp)
    print("voltage:", robot.voltage)
    print("power:", robot.power)
    print("current:", robot.current)
    # print("M_A_mode:", robot.M_A_mode)


    """プロジェクト書き換え、現在のプロジェクト確認"""
    robot.set_project("amrdemo1")
    print("current_project",robot.current_project)
    robot.set_task_speed(10)
    robot.task_start()
    time.sleep(2)
    while robot.project_run :
        print("タスク実行中")
        time.sleep(1)

    robot.task_stop()

    time.sleep(3)
    robot.set_project("amrdemo2")
    print("current_project",robot.current_project)
    robot.set_task_speed(10)
    robot.task_start()
    time.sleep(2)
    while robot.project_run :
        print("タスク実行中")
        time.sleep(1)

    robot.task_stop()

    # """タスクの停止"""
    # robot.task_stop()


    # """オートモード確認"""
    # print("robot_mode",robot.M_A_mode)
    # robot.enable_auto_mode()
    # print(robot.auto_mode)
    # robot.disable_auto_mode()
    # print(robot.auto_mode)

    # """プロジェクト実行中確認"""
    # print("プロジェクト実行中 : ", robot.project_run)
    # print("プロジェクト編集中 : ", robot.project_edit)
    # print("プロジェクト一時停止中 : ", robot.project_pause)