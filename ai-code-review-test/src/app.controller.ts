import { Controller, Get, Request, UseGuards } from '@nestjs/common';
import { AppService } from './app.service';
import { AuthGuard } from '@nestjs/passport';

@Controller()
export class AppController {
    constructor(private readonly appService: AppService) {}

    // 메인 페이지에서 API 목록, 사용자 할 일 통계, 전체 유저 수를 반환
    @UseGuards(AuthGuard('jwt')) // 사용자 인증 후 접근 가능
    @Get()
    async getAppInfo(@Request() req) {
        const apiList = this.appService.getApiList();
        const todoStats = await this.appService.getUserTodoStats(req.user.userId);
        const userCount = await this.appService.getTotalUserCount();

        return {
            apiList,
            todoStats,
            userCount,
        };
    }
}
