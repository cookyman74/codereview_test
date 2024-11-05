import { Injectable } from '@nestjs/common';
import { PrismaService } from "./prisma/prisma.service";

@Injectable()
export class AppService {
    constructor(private prisma: PrismaService) {}

    getApiList() {
        return [
            { method: 'GET', url: '/auth/login', description: '로그인' },
            { method: 'POST', url: '/todos', description: '할 일 생성' },
            { method: 'GET', url: '/todos', description: '할 일 목록 조회' },
            { method: 'DELETE', url: '/todos/:id', description: '할 일 삭제' },
        ];
    }

    // 사용자별 할 일 통계 계산 (총 할 일 수, 완료된 할 일 수)
    async getUserTodoStats(userId: number) {
        const totalTodos = await this.prisma.todo.count({
            where: { userId },
        });

        const completedTodos = await this.prisma.todo.count({
            where: { userId, completed: true },
        });

        return {
            totalTodos,
            completedTodos,
        };
    }

    // 전체 유저 수 반환
    async getTotalUserCount() {
        return this.prisma.user.count();
    }
}
