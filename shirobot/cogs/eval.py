import asyncio
import discord
from discord.ext import commands


def to_code(argument):
    print(argument)
    argument = argument.removeprefix("```py")
    argument = argument.removesuffix("```")
    argument = argument.strip()
    return argument


class EvalCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval")
    async def eval_cmd(self, ctx, *, code: to_code):
        print(code)
        await ctx.send(
            view=EvalView(ctx=ctx, code=code),
        )


class EvalView(discord.ui.View):
    def __init__(self, ctx, code):
        super().__init__()
        self.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="Code",
                url=ctx.message.jump_url,
            )
        )
        self.code = code
        self.task = None

    @discord.ui.button(
        style=discord.ButtonStyle.grey,
        label="Run",
        custom_id="run",
        emoji=discord.PartialEmoji.from_str("<:run:1208545878801911849>"),
    )
    async def run(self, button, interaction):
        async def run_code(interaction, view):
            embed = discord.Embed()
            embed.title = "Output"
            embed.description = (
                f"```py\n{self.code}\n```"  # TODO: Replace with the output of the code
            )
            view.get_item(custom_id="abort").disabled = True
            view.get_item(custom_id="run").label = "Rerun"
            view.get_item(custom_id="run").disabled = False

            await asyncio.sleep(5)  # TODO: Replace with an actual eval

            await interaction.followup.edit_message(
                interaction.message.id, embed=embed, view=view
            )

            print("done")

        self.task = asyncio.create_task(run_code(interaction, self))
        self.get_item(custom_id="abort").disabled = False
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(
        style=discord.ButtonStyle.grey,
        label="Abort",
        custom_id="abort",
        emoji=discord.PartialEmoji.from_str("<:stop:1208545916219432960>"),
        disabled=True,
    )
    async def abort(self, button, interaction):
        if not self.task:
            return

        self.task.cancel()
        self.task = None

        self.get_item(custom_id="run").disabled = False
        button.disabled = True
        await interaction.response.edit_message(view=self)


def setup(bot):
    bot.add_cog(EvalCommand(bot))
